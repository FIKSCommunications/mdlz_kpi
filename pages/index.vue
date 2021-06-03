<template>
  <div>
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            集計期間
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols=3 class="mb-0 pb-0">
                <v-text-field
                  v-model="startDt"
                  label="開始日"
                  outlined
                  type="month"
                  dense
                  hide-details
                  @change="getSearchOption"
                ></v-text-field>
              </v-col>
              <v-col cols=3 class="mb-0 pb-0">
                <v-text-field
                  v-model="endDt"
                  label="終了日"
                  outlined
                  type="month"
                  dense
                  hide-details
                  @change="getSearchOption"
                ></v-text-field>
              </v-col>
            </v-row>
            <!--v-row v-show="viewFlgSummary">
              <v-col cols="12">
              <v-text-field
                label="企業検索"
                v-model="psearch"
                outlined
                dense
              ></v-text-field>
              </v-col>
            </v-row-->
            <v-row>
              <v-col class="my-0 py-0">
                <v-select
                  v-model="checkedHonbu"
                  multiple
                  label="営業本部"
                  item-text="label"
                  :items="selectHonbu"
                >
                </v-select>
              </v-col>
              <v-col class="my-0 py-0">
                <v-select
                  v-model="checkedGroup"
                  multiple
                  label="グループ"
                  item-text="label"
                  :items="selectGroup"
                >
                </v-select>
              </v-col>
              <v-col class="my-0 py-0">
                <!-- <v-select
                  v-model="checkedSales"
                  multiple
                  label="セールス"
                  item-text="label"
                  :items="selectSales"
                >
                </v-select> -->
                <fiks-multiselectbox-component
                  @input="selected_sales_update"  
                  label="セールス" :listOptions="selectSales">
                </fiks-multiselectbox-component>
              </v-col>
              <v-col class="my-0 py-0">
                <v-select
                  v-model="checkedChanel"
                  multiple
                  label="チャネル"
                  item-text="label"
                  :items="selectChanel"
                >
                </v-select>
              </v-col>
              <v-col class="my-0 py-0">
                <!-- <v-select
                  v-model="checkedChq"
                  multiple
                  label="企業名"
                  item-text="label"
                  :items="selectChq"
                >
                </v-select> -->
                <fiks-multiselectbox-component
                  @input="selected_chq_update"  
                  label="企業名" :listOptions="selectChq">
                </fiks-multiselectbox-component>
              </v-col>
            </v-row>
            <v-row>
              <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  class="mr-2 mb-2"
                  @click="clickAggregate"
                >
                  集計
                </v-btn>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- shop -->
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="12">
        <summaryGraph
        regi="none"
        categoryFlg="none"
        :title="visitData.title"
        :cols="visitData.cols"
        :summary="visitData.summary"
        :detail="visitData.detail"
        :loading="visitData.loading"
        :psearch="psearch"
        >
        </summaryGraph>
      </v-col>
    </v-row>

    <!-- call -->
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="12">
        <summaryGraph
        regi="none"
        categoryFlg="none"
        :title="callData.title"
        :cols="callData.cols"
        :summary="callData.summary"
        :detail="callData.detail"
        :loading="callData.loading"
        :psearch="psearch"
        >
        </summaryGraph>
      </v-col>
    </v-row>

    <!-- 1.hz -->
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="12">
        <summaryGraph
        regi="true"
        categoryFlg="true"
        :title="hzGetData.title"
        :cols="hzGetData.cols"
        :summary="hzGetData.summary"
        :detail="hzGetData.detail"
        :loading="hzGetData.loading"
        :psearch="psearch"
        >
        </summaryGraph>
      </v-col>
    </v-row>

    <!-- 2.hzall -->
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="12">
        <summaryGraph
        regi="none"
        categoryFlg="true"
        :title="hzAllData.title"
        :cols="hzAllData.cols"
        :summary="hzAllData.summary"
        :detail="hzAllData.detail"
        :loading="hzAllData.loading"
        :psearch="psearch"
        >
        </summaryGraph>
      </v-col>
    </v-row>

    <!-- 3.sd -->
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="12">
        <summaryGraph
        regi="none"
        categoryFlg="true"
        :title="sdAllData.title"
        :cols="sdAllData.cols"
        :summary="sdAllData.summary"
        :detail="sdAllData.detail"
        :loading="sdAllData.loading"
        :psearch="psearch"
        >
        </summaryGraph>
      </v-col>
    </v-row>

    <!-- 4.dp -->
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="12">
        <summaryGraph
        regi="none"
        categoryFlg="true"
        :title="dpData.title"
        :cols="dpData.cols"
        :summary="dpData.summary"
        :detail="dpData.detail"
        :loading="dpData.loading"
        :psearch="psearch"
        >
        </summaryGraph>
      </v-col>
    </v-row>

    <!-- 5.display -->
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="12">
        <summaryGraph
        regi="none"
        categoryFlg="true"
        :title="displayData.title"
        :cols="displayData.cols"
        :summary="displayData.summary"
        :detail="displayData.detail"
        :loading="displayData.loading"
        :psearch="psearch"
        >
        </summaryGraph>
      </v-col>
    </v-row>

  </div>
</template>

<script>
import moment from "moment";
import summaryGraph from "../components/summaryGraph";
import multiSelect from "../components/FiksMultiselectboxComponent.vue";
import axios from 'axios'
export default {
  components:{
    summaryGraph,
  },
  data () {
    return {
      psearch:'',

      selectHonbu:[],
      selectGroup:[],
      selectSales:[],
      selectChanel:[],
      selectChq:[],

      checkedHonbu:[],
      checkedGroup:[],
      checkedSales:[],
      checkedChanel:[],
      checkedChq:[],

      visitData:{
        id:11,
        title:'■　全体カバレッジ',
        cols:[
              {text:'企業',value:'chq'},
              {text:'設定店舗数',value:'all',align:'end'},
              {text:'訪問店舗数',value:'num',align:'end'},
              {text:'カバー率',value:'rate',align:'end'},
              ],
        summary:[],
        detail:[],
        loading:false,
      },

      callData:{
        id:12,
        title:'■　全体コール',
        cols:[
              {text:'企業',value:'chq'},
              {text:'設定コール数',value:'all',align:'end'},
              {text:'訪問コール数',value:'num',align:'end'},
              {text:'コール率',value:'rate',align:'end'},
              ],
        summary:[],
        detail:[],
        loading:false,
      },

      hzGetData:{
        id:1,
        title:'①　HZ占有率',
        cols:[
              {text:'企業',value:'chq'},
              {text:'カテゴリー',value:'category'},
              {text:'ターゲット',value:'all',align:'end'},
              {text:'レジ台数',value:'regi',align:'end'},
              {text:'拠点数',value:'num',align:'end'},
              {text:'カバレッジ',value:'cavarege',align:'end'},
              {text:'達成率',value:'rate',align:'end'},
              ],
        summary:[],
        detail:[],
        loading:false,
      },
      hzAllData:{
        id:2,
        title:'②　HZ総拠点数',
        cols:[
              {text:'企業',value:'chq'},
              {text:'カテゴリー',value:'category'},
              {text:'ターゲット',value:'all',align:'end'},
              {text:'拠点数',value:'num',align:'end'},
              {text:'達成率',value:'rate',align:'end'},
              ],
        summary:[],
        detail:[],
        loading:false,
      },
      sdAllData:{
        id:3,
        title:'③　SD総拠点数',
        cols:[
              {text:'企業',value:'chq'},
              {text:'カテゴリー',value:'category'},
              {text:'ターゲット',value:'all',align:'end'},
              {text:'拠点数',value:'num',align:'end'},
              {text:'達成率',value:'rate',align:'end'},
              ],
        summary :[],
        detail:[],
        loading:false,
      },
      dpData:{
        id:4,
        title:'④　DP設置台数',
        cols:[
              {text:'企業',value:'chq'},
              {text:'カテゴリー',value:'category'},
              {text:'ターゲット',value:'all',align:'end'},
              {text:'設置台数',value:'num',align:'end'},
              {text:'達成率',value:'rate',align:'end'},
              ],
        summary:[],
        detail:[],
        loading:false,
      },
      displayData:{
        id:5,
        title:'⑤　大陳数',
        cols:[
              {text:'企業',value:'chq'},
              {text:'カテゴリー',value:'category'},
              {text:'ターゲット',value:'all',align:'end'},
              {text:'大陳回数',value:'num',align:'end'},
              {text:'達成率',value:'rate',align:'end'},
              ],
        summary:[],
        detail:[],
        loading:false,
      },
      startDt:moment(new Date).startOf("month").format('YYYY-MM'),
      endDt:moment(new Date).endOf("month").format('YYYY-MM'),
      viewFlgSummary:false,
    }
  },
  created: function() {
    // 検索オプションの取得
    this.getSearchOption();
  },
  methods:{
    getSearchOption(){
      const initFile = '/kpi_summaryinit_ajax.php';
      let url = this.$urls.proPythonUrl + initFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + initFile;
      }
      let that = this;
      axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        that.selectHonbu = response.data.honbu;
        that.selectGroup = response.data.group;
        that.selectChanel = response.data.chanel;
        that.selectSales = response.data.sales;
        that.selectChq = response.data.chqname;
      })
      .catch(function(error){
        console.log(error);
        alert('検索項目の取得に失敗しました')
        that.selectHonbu = [];
        that.selectGroup = [];
        that.selectChanel = [];
        that.selectSales = [];
        that.selectChq = [];
      });
    },
    // 集計ボタン
    clickAggregate(){
      if (this.startDt > this.endDt) {
        alert('日付が不正です');
        return false;
      }
      this.viewFlgSummary = true;
      this.calcVisitGetData();
      this.calcCallGetData();
      this.calcHzGetData();
      this.calcHzAllGetData();
      this.calcSdAllGetData() ;
      this.calcDpGetData();
      this.calcDisplayGetData();
    },

    // 訪問店舗数
    calcVisitGetData(){
      const visitFile = '/kpi_summaryshop_ajax.php';
      this.visitData.loading = true;
      let url = this.$urls.proPythonUrl + visitFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + visitFile;
      }

      let that = this;
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
          'checkedChq': this.checkedChq,
        },
        /*
        paramsSerializer: (params) => {
          return qs.stringify(params, { arrayFormat: 'repeat'});
        },
        */

      })
      .then(function(response){
        that.visitData.summary = response.data.summary;
        that.visitData.detail = response.data.detail
      })
      .catch(function(error){
        console.log(error);
        alert('訪問店舗数の集計に失敗しました')
        that.visitData.summary = [];
        that.visitData.detail = [];
      })
      .finally(function(){
        that.visitData.loading = false;        
      });
    },

    // 訪問店舗数
    calcCallGetData(){
      const callFile = '/kpi_summarycall_ajax.php';
      this.callData.loading = true;
      let url = this.$urls.proPythonUrl + callFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + callFile;
      }

      let that = this;
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
          'checkedChq': this.checkedChq,
        }
      })
      .then(function(response){
        that.callData.summary = response.data.summary;
        that.callData.detail = response.data.detail
      })
      .catch(function(error){
        console.log(error);
        alert('コール数の集計に失敗しました')
        that.callData.summary = [];
        that.callData.detail = [];
      })
      .finally(function(){
        that.callData.loading = false;        
      });
    },


    // 1.HZ占有率
    calcHzGetData(){
      const hzFile = '/kpi_summary1_ajax.php';
      this.hzGetData.loading = true;
      let url = this.$urls.proPythonUrl + hzFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + hzFile;
      }

      let that = this;
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
          'checkedChq': this.checkedChq,
        }
      })
      .then(function(response){
        that.hzGetData.summary = response.data.summary;
        that.hzGetData.detail = response.data.detail
      })
      .catch(function(error){
        console.log(error);
        alert('HZ占有率の集計に失敗しました')
        that.hzGetData.summary = [];
        that.hzGetData.detail = [];
      })
      .finally(function(){
        that.hzGetData.loading = false;        
      });
    },

    // 2.HZ総拠点数
    calcHzAllGetData(){
      const hzallFile = '/kpi_summary2_ajax.php';
      this.hzAllData.loading = true;
      let url = this.$urls.proPythonUrl + hzallFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + hzallFile;
      }

      let that = this;
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
          'checkedChq': this.checkedChq,
        }
      })
      .then(function(response){
        that.hzAllData.summary = response.data.summary;
        that.hzAllData.detail = response.data.detail
      })
      .catch(function(error){
        console.log(error);
        alert('HZ総拠点数の集計に失敗しました')
        that.hzAllData.summary = [];
        that.hzAllData.detail = [];
      })
      .finally(function(){
        that.hzAllData.loading = false;        
      });
    },

    // 3.SD総拠点数
    calcSdAllGetData(){
      const sdallFile = '/kpi_summary3_ajax.php';
      this.sdAllData.loading = true;
      let url = this.$urls.proPythonUrl + sdallFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + sdallFile;
      }

      let that = this;
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
          'checkedChq': this.checkedChq,
        }
      })
      .then(function(response){
        that.sdAllData.summary = response.data.summary;
        that.sdAllData.detail = response.data.detail
      })
      .catch(function(error){
        console.log(error);
        alert('SD総拠点数の集計に失敗しました')
        that.sdAllData.summary = [];
        that.sdAllData.detail = [];
      })
      .finally(function(){
        that.sdAllData.loading = false;        
      });
    },

    // 4.DP設置台数
    calcDpGetData(){
      const dpFile = '/kpi_summary4_ajax.php';
      this.dpData.loading = true;
      let url = this.$urls.proPythonUrl + dpFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + dpFile;
      }

      let that = this
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
          'checkedChq': this.checkedChq,
        }
      })
      .then(function(response){
        that.dpData.summary = response.data.summary;
        that.dpData.detail = response.data.detail;
      })
      .catch(function(error){
        console.log(error);
        alert('DP設置台数の集計に失敗しました')
        that.dpData.summary = [];
        that.dpData.detail = [];
      })
      .finally(function(){
        that.dpData.loading = false;        
      });
    },

    // 5.大陳列
    calcDisplayGetData(){
      const displayFile = '/kpi_summary5_ajax.php';
      this.displayData.loading = true;
      let url = this.$urls.proPythonUrl + displayFile;
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + displayFile;
      }

      let that = this;
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
          'checkedChq': this.checkedChq,
        }
      })
      .then(function(response){
        that.displayData.summary = response.data.summary;
        that.displayData.detail = response.data.detail;
      })
      .catch(function(error){
        console.log(error);
        alert('大陳数の集計に失敗しました')
        that.displayData.summary = [];
        that.displayData.detail = [];
      })
      .finally(function(){
        that.displayData.loading = false;        
      });
    },    
    selected_sales_update(value) {
      this.checkedSales = value
    },
    selected_chq_update(value) {
      this.checkedChq = value
    },
    // 5.大陳列ログバージョン 使っていない
    /*
    calcDisplayGetData_log(){
      this.displayData.loading = true;
      this.displayData.all = 0;
      this.displayData.num = 0;
      this.displayData.rate = 0;
      this.displayData.detail = [];
      let url = this.$urls.proPythonUrl + '/kpi_summary5log.py';
      if (this.$urls.envFlg === 'dev') {
        url = this.$urls.devPythonUrl + '/kpi_summary5log.py';
      }
      const response = axios.get(url, {
        //timeout: 30000,
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
          'checkedHonbu': this.checkedHonbu,
          'checkedGroup': this.checkedGroup,
          'checkedSales': this.checkedSales,
          'checkedChanel': this.checkedChanel,
        }
      })
      .then(function(data){
        if (data.data.summary) {
          // logから取得
            this.displayData.all = data.data.summary.all;
            this.displayData.num = data.data.summary.num;
            this.displayData.rate = data.data.summary.rate;
            this.displayData.detail = data.data.detail;
            this.displayData.loading = false;        
            return false
        } else {
          // 再計算

          if (data.data.result) {

            // 更新チェック処理　ここから
            console.log(data.data.detail); //keyid

            const numOfTime = 10; // ループ数
            const delay = 10000; // スリーブ時間 ms

            // 条件
            let t = this
            const judge = function(r,t) {
                if(r.data.result == 'done') {
                  const j = JSON.parse(r.data.detail)
                  t.displayData.all = j.summary.all;
                  t.displayData.num = j.summary.num;
                  t.displayData.rate = j.summary.rate;
                  t.displayData.detail = j.detail;
                  return true;
                }
                return false;
            };

            // スリーブ
            function sleep(time) {
                return new Promise((resolve, reject) => {
                    setTimeout(() => {
                        resolve();
                    }, time);
                });
            }

            let watchurl = this.$urls.proPythonUrl + '/kpi_summary5watch.py';
            if (this.$urls.envFlg === 'dev') {
              watchurl = this.$urls.devPythonUrl + '/kpi_summary5watch.py';
            }

            // ループ
            const loopFunc = async (delay, numOfTime, judge) => {
                const arr = Array.from({length: numOfTime}, (v, k) => k);
                for(let i of arr){
                    let r = await axios.get(watchurl,{
                      params:{ 'keyid': data.data.detail }
                    })
                    .then(function (response) {
                        console.log(i, response);
                        return Promise.resolve(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                    // 条件処理を追加
                    if(judge(r,t)){
                        return Promise.resolve(1);
                    }                  
                    await sleep(delay);
                } 
            };
            loopFunc(delay, numOfTime, judge).then(()=>{
                console.log('done!!');
                this.displayData.loading = false; 
            });

            // 更新チェック処理　ここまで

          } else {
            alert('失敗')
            this.displayData.loading = false;        
          }         

        }
      }.bind(this))
      .catch(function(error){
        console.log(error);
        this.displayData.loading = false;        
      }.bind(this));
    },
    */

  },
}
</script>
