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
                        <td>{{ all | addComma }}</td>
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
            <v-col cols="4">
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
                    <td>{{ data.all | addComma }}</td>
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
