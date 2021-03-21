<template>
  <v-card>
    <v-overlay 
     absolute
     :value="overlay"
    >
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

    <v-card-title>
      {{title}}
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col>
          <v-row>
            <v-col cols="12">
              <v-sheet
                color="white"
                elevation="2"
              >
                <v-simple-table dense>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th v-for="(col, index) in cols" :key="index" class="text-left">
                          {{col}}
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{{ all | addComma }}<span v-if="regi!='none'">%</span></td>
                        <td v-if="regi!='none'">{{ regi | addComma }}</td>
                        <td>{{ num | addComma }}</td>
                        <td v-if="cavarege!='none'">{{ cavarege | orgRound(10) }}%</td>
                        <td>{{ rate | orgRound(10) }}%</td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-sheet>
            </v-col>
          </v-row>
          <v-row justify="end" align="center">
            <v-col cols="6">
              <v-btn 
              color="primary" 
              rounded 
              small  
              text
              class="text-decoration-underline"
              @click="viewDetail"
              >
              <v-icon x-small>{{viewFlg==false?'mdi-plus':'mdi-minus'}}</v-icon>
              {{viewFlg==false?'詳細':'詳細非表示'}}</v-btn>
            </v-col>
            <v-col cols="6" align="end">
              <v-btn 
              color="primary" 
              rounded 
              small  
              text
              class="text-decoration-underline"
              @click="downloadCSV"
              >
              ダウンロード</v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row v-show="viewFlg">
        <v-col cols="12">
          <v-sheet
            color="white"
            elevation="2"
          >
            <v-simple-table 
            dense
            fixed-header
            >
              <template v-slot:default>
                <thead>
                  <tr>
                    <th>企業</th>
                    <th v-for="(col, index) in cols" :key="index" class="text-left">
                      {{col}}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(data, index) in detalData" :key="index">
                    <td>{{data.chq}}</td>
                    <td>{{ data.all | addComma }}<span v-if="regi!='none'">%</span></td>
                    <td v-if="regi!='none'">{{ data.regi | addComma }}</td>
                    <td>{{ data.num | addComma }}</td>
                    <td v-if="cavarege!='none'">{{ data.cavarege | orgRound(10) }}%</td>
                    <td>{{ data.rate | orgRound(10) }}%</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-sheet>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      viewFlg : false,
      detalData : [],
      overlay: false,
    }
  },
  watch:{
    detail: function(){
      console.log('detail change');
      this.detalData = this.detail;
    },
    loading: function(){
      console.log('loading change');
      this.overlay = this.loading;
    }
  },
  methods:{
    viewDetail:function(){
      if (this.viewFlg == true) {
        this.viewFlg = false;
      } else {
        this.viewFlg = true;
      }
    },
    downloadCSV:function(){
      //let csv = '\ufeff' + '企業,';

      //全体
      let head = '\ufeff';
      this.cols.forEach(el => {
        head += el + ',';
      });      
      head = head.slice(0, -1) + '\n';
      let csv = head;
      if (this.regi != 'none') {
        csv += this.all +','+ this.regi +','+ this.num +','+  Math.round(this.cavarege*10)/10 +','+  Math.round(this.rate*10)/10 + '\n\n';
      } else {
        csv += this.all +','+ this.num +','+  Math.round(this.rate*10)/10 + '\n\n';
      }

      //企業別
      csv += '企業,' + head;
      this.detalData.forEach(el => {
        let line = '';
        if (this.regi != 'none') {
          line = '"' + el['chq'] +'",'+ el['all'] +','+ el['regi'] +','+ el['num'] +','+  Math.round(el['cavarege']*10)/10 +','+  Math.round(el['rate']*10)/10 + '\n';
        } else {
          line = '"' + el['chq'] +'",'+ el['all'] +','+ el['num'] +','+  Math.round(el['rate']*10)/10 + '\n';
        }
        csv += line;
      })
      let blob = new Blob([csv], { type: 'text/csv' })
      let link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = this.title + '.csv';
      link.click()      
    },
  },
  filters:{
    addComma: function(value) {
      if (! value) return value;
      let formatter = new Intl.NumberFormat('ja-JP')
      return formatter.format(value)
      //return value.toLocaleString();
    },
    orgRound: function(value, base) {
      if (! value) return value;
      return Math.round(value * base) / base;
    },
    addPercent: function(value) {
      return value + '%';
    }
  },
  props:[
    'title',
    'cols',
    'all',
    'rate',
    'num',
    'regi',
    'cavarege',
    'detail',
    'loading',
  ]
}
</script>
