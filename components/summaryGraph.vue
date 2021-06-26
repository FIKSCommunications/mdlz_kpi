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
                        <th v-for="(col, index) in cols" :key="index" :class="{ 'text-right': 'align' in col }">
                          {{ col.text }}
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(sum, index) in summary" :key="index">
                        <td>*</td>
                        <td v-if="categoryFlg!='none'">{{ sum.category }}</td>
                        <td class="text-right">{{ sum.all | orgRound(regi) }}<span v-if="regi!='none'">%</span></td>
                        <td class="text-right" v-if="regi!='none'">{{ sum.regi | addComma }}</td>
                        <td class='text-right'>{{ sum.num | addComma }}</td>
                        <td class="text-right" v-if="regi!='none'">{{ sum.cavarege | orgRound(regi) }}%</td>
                        <td :class="{ 'light-blue lighten-4' : sum.rate >= 100, 'text-right' : true  }">{{ sum.rate | orgRound }}%</td>
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
            <v-data-table
            :headers="cols"
            :items="detalData"
            disable-pagination
            hide-default-footer
            dense
            :search="search"
            :sort-by="['chq']"
            >
            <template v-slot:item="{ item }">
              <tr :class="{ 'yellow lighten-5' : item.category==='ANY' && categoryFlg!=='none' }">
                <td>{{ item.chq }}</td>
                <td v-if="categoryFlg!='none'">{{ item.category }}</td>
                <td class="text-right">
                  {{ item.all | orgRound(regi) }}<span v-if="regi!='none'">%</span>
                </td>
                <td class="text-right" v-if="regi!='none'">
                  {{ item.regi | addComma }}
                </td>
                <td class="text-right">
                  {{ item.num | addComma }}
                </td>
                <td class="text-right" v-if="regi!='none'">
                  {{ item.cavarege | orgRound }}%
                </td>
                <td class="text-right">
                  <div :class="{ 'light-blue lighten-4' : item.rate >= 100  }">{{ item.rate | orgRound }}%</div>
                </td>
              </tr>
            </template>
              <!--template v-slot:item.all="{ item }">
                {{ item.all | orgRound(regi) }}<span v-if="regi!='none'">%</span>
              </template>
              <template v-slot:item.regi="{ item }">
                {{ item.regi | addComma }}
              </template>
              <template v-slot:item.num="{ item }">
                {{ item.num | addComma }}
              </template>
              <template v-slot:item.cavarege="{ item }">
                {{ item.cavarege | orgRound }}%
              </template>
              <template v-slot:item.rate="{ item }">
                <div :class="{ 'light-blue lighten-4' : item.rate >= 100  }">{{ item.rate | orgRound }}%</div>
              </template-->
            </v-data-table>
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
      search:'',
    }
  },
  watch:{
    detail: function(){
      this.detalData = this.detail;
    },
    loading: function(){
      this.overlay = this.loading;
    },
    psearch: function(){
      this.search = this.psearch;
      this.viewFlg = true;
    }
  },
  methods:{
    // 小数点１桁表示
    decimalRound(value) {
      return (Math.round(value * Math.pow(10, 1))/Math.pow(10, 1)).toFixed(1);
    },

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
        head += el.text + ',';
      });      
      head = head.slice(0, -1) + '\n';
      let csv = head;
      /*
      if (this.regi != 'none') {
        csv += '"全体",' + this.all.toFixed(1) +','+ this.regi +','+ this.num +','+  this.cavarege.toFixed(1) +','+  this.rate.toFixed(1) + '\n\n';
      } else {
        csv += '"全体",' + this.all.toFixed(0) +','+ this.num +','+  this.rate.toFixed(1) + '\n\n';
      }
      */
      this.summary.forEach(el => {
        if (this.regi != 'none') {
          //csv += '"全体","' + el['category'] + '",' + el['all'].toFixed(1) +','+ el['regi'] +','+ el['num'] +','+  el['cavarege'].toFixed(1) +','+ el['rate'].toFixed(1) + '\n\n';
          csv += '"全体",' + (this.categoryFlg!='none' ? '"'+el['category']+'",' : '') + this.decimalRound(el['all']) +','+ el['regi'] +','+ el['num'] +','+  this.decimalRound(el['cavarege']) +','+ this.decimalRound(el['rate']) + '\n';
        } else {
          //csv += '"全体","' + el['category'] + '",' + el['all'].toFixed(0) +','+ el['num'] +','+ el['rate'].toFixed(1) + '\n\n';
          csv += '"全体",' + (this.categoryFlg!='none' ? '"'+el['category']+'",' : '') + Math.round(el['all']) +','+ el['num'] +','+ this.decimalRound(el['rate']) + '\n';
        }
      });
      csv += '\n';

      //企業別
      csv += head;
      this.detalData.forEach(el => {
        let line = '';
        if (this.regi != 'none') {
          //line = '"' + el['chq'] +'",'+ el['category'] +'",'+ el['all'].toFixed(1) +','+ el['regi'] +','+ el['num'] +','+  el['cavarege'].toFixed(1) +','+  el['rate'].toFixed(1) + '\n';
          line = '"' + el['chq'] +'",'+ (this.categoryFlg!='none' ? '"'+el['category']+'",' : '') + this.decimalRound(el['all']) +','+ el['regi'] +','+ el['num'] +','+  this.decimalRound(el['cavarege']) +','+  this.decimalRound(el['rate']) + '\n';
        } else {
          //line = '"' + el['chq'] +'",'+ el['category'] +'",'+ el['all'].toFixed(0) +','+ el['num'] +','+  el['rate'].toFixed(1) + '\n';
          line = '"' + el['chq'] +'",'+ (this.categoryFlg!='none' ? '"'+el['category']+'",' : '') + Math.round(el['all']) +','+ el['num'] +','+  this.decimalRound(el['rate']) + '\n';
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
    },

    // 小数点１桁表示、カンマ区切り
    orgRound: function(value, regi) {
      let ret;
      if (value === 0 || !value) {
        if (regi !== 'none') {
          return '0.0';
        } else {
          return '0';
        }
      }

      // 少数点1桁四捨五入
      if (regi !== 'none') {
        //ret = parseFloat(value).toFixed(1);
        ret =  (Math.round(value * Math.pow(10, 1))/Math.pow(10, 1)).toFixed(1);
        //ret = this.decimalRound(value);
      } else {
        // カンマ区切り
        //ret = value.toFixed(0);
        ret = (Math.round(value)).toFixed(1);

        let formatter = new Intl.NumberFormat('ja-JP');
        ret = formatter.format(ret);
      }
      return ret;
    },

    addPercent: function(value) {
      return value + '%';
    },
  },
  props:[
    'title',
    'cols',
    'regi',
    'categoryFlg',
    'summary',
    'detail',
    'loading',
    'psearch',
  ]
}
</script>
