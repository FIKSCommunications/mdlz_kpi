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
                        <td>{{ all }}</td>
                        <td v-show="regi!='none'">{{ regi }}</td>
                        <td>{{ num }}</td>
                        <td v-show="cavarege!='none'">{{ cavarege }}</td>
                        <td>{{ rate }}%</td>
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
        <!-- <v-col class=mt-3>
          <v-progress-linear
            :value="rate"
            :color="rate >= 100 ? 'green' : 'warning' "
            height="20"
          >
            <strong>{{rate}}%</strong>
          </v-progress-linear>
        </v-col> -->
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
                    <td>{{ data.all }}</td>
                    <td v-show="regi!='none'">{{ data.regi }}</td>
                    <td>{{ data.num }}</td>
                    <td v-show="cavarege!='none'">{{ data.cavarege }}</td>
                    <td>{{ data.rate }}%</td>
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
      console.log('props change');
      console.log(this.detail);
      this.detalData = this.detail;
    },
    loading: function(){
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
      console.log(this.viewFlg)
    },
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
