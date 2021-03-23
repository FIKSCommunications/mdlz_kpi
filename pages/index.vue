<template>
  <div>
    <v-row justify="center" align="center">
      <v-col cols="8">
        <v-card>
          <v-card-title>
            集計期間
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols=5>
                <v-text-field
                  v-model="startDt"
                  label="開始日"
                  outlined
                  type="month"
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols=5>
                <v-text-field
                  v-model="endDt"
                  label="終了日"
                  outlined
                  type="month"
                  dense
                ></v-text-field>
              </v-col>
              <v-col>
                <v-btn
                  color="primary"
                  @click="clickAggregate"
                >
                  集計
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <summaryGraph
        :title="hzGetData.title"
        :cols="hzGetData.cols"
        :all="hzGetData.all"
        :rate="hzGetData.rate"
        :num="hzGetData.num"
        :regi="hzGetData.regi"
        :cavarege="hzGetData.cavarege"
        :detail="hzGetData.detail"
        :loading="hzGetData.loading"
        >
        </summaryGraph>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <summaryGraph
        :title="hzAllData.title"
        :cols="hzAllData.cols"
        :all="hzAllData.all"
        :rate="hzAllData.rate"
        :num="hzAllData.num"
        regi="none"
        cavarege="none"
        :detail="hzAllData.detail"
        :loading="hzAllData.loading"
        >
        </summaryGraph>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <summaryGraph
        :title="sdAllData.title"
        :cols="sdAllData.cols"
        :all="sdAllData.all"
        :rate="sdAllData.rate"
        :num="sdAllData.num"
        regi="none"
        cavarege="none"
        :detail="sdAllData.detail"
        :loading="sdAllData.loading"
        >
        </summaryGraph>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <summaryGraph
        :title="dpData.title"
        :cols="dpData.cols"
        :all="dpData.all"
        :rate="dpData.rate"
        :num="dpData.num"
        regi="none"
        cavarege="none"
        :detail="dpData.detail"
        :loading="dpData.loading"
        >
        </summaryGraph>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <summaryGraph
        :title="displayData.title"
        :cols="displayData.cols"
        :all="displayData.all"
        :rate="displayData.rate"
        :num="displayData.num"
        regi="none"
        cavarege="none"
        :detail="displayData.detail"
        :loading="displayData.loading"
        >
        </summaryGraph>
      </v-col>
    </v-row>
    <!--v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <summaryGraph
        :title="inproData.title"
        :cols="inproData.cols"
        :all="inproData.all"
        :rate="inproData.rate"
        :num="inproData.num"
        regi="none"
        cavarege="none"
        :detail="inproData.detail"
        :loading="inproData.loading"
        >
        </summaryGraph>
      </v-col>
    </v-row-->
  </div>
</template>

<script>
import moment from "moment";
import summaryGraph from "../components/summaryGraph";
import axios from 'axios'
export default {
  components:{
    summaryGraph,
  },
  data () {
    return {
      hzGetData:{
        id:1,
        title:'①　HZ占有率',
        cols:['ターゲット','レジ台数','拠点数','カバレッジ','達成率'],
        all :0,
        num  :0,
        regi:0,
        cavarege:0,
        rate:0,
        detail:[],
        loading:false,
      },
      hzAllData:{
        id:2,
        title:'②　HZ総拠点数',
        cols:['ターゲット','拠点数','達成率'],
        all :0,
        num  :0,
        rate:0,
        detail:[],
        loading:false,
      },
      sdAllData:{
        id:3,
        title:'③　SD総拠点数',
        cols:['ターゲット','拠点数','達成率'],
        all :0,
        num  :0,
        rate:0,
        detail:[],
        loading:false,
      },
      dpData:{
        id:4,
        title:'④　DP設置台数',
        cols:['ターゲット','設置台数','達成率'],
        all :0,
        num  :0,
        rate:0,
        detail:[],
        loading:false,
      },
      displayData:{
        id:5,
        title:'⑤　大陳列',
        cols:['ターゲット','大陳回数','達成率'],
        all :0,
        num  :0,
        rate:0,
        detail:[],
        loading:false,
      },
      inproData:{
        id:6,
        title:'⑥　インプロ金額',
        cols:['ターゲット','インプロ金額','達成率'],
        all :0,
        num  :0,
        rate:0,
        detail:[],
        loading:false,
      },
      startDt:moment(new Date).startOf("month").format('YYYY-MM'),
      endDt:moment(new Date).endOf("month").format('YYYY-MM'),
      viewFlgSummary:false,
    }
  },
  methods:{
    clickAggregate(){
      if (this.startDt > this.endDt) {
        alert('日付が不正です');
        return false;
      }
      this.viewFlgSummary = true;
      this.calcHzGetData();
      this.calcHzAllGetData();
      this.calcSdAllGetData() ;
      this.calcDpGetData();
      this.calcDisplayGetData();
      //6は未完成のため除く
      //this.calcInproGetData();
    },
    // 1.HZ占有率
    calcHzGetData(){
      this.hzGetData.loading = true;
      //let url = 'http://localhost:8080/cgi-bin/kpi_summary1.py';
      let url = 'server/cgi-bin/kpi_summary1.py';
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        this.hzGetData.all = response.data.summary.all;
        this.hzGetData.regi = response.data.summary.regi;
        this.hzGetData.num = response.data.summary.num;
        this.hzGetData.cavarege = response.data.summary.cavarege;
        this.hzGetData.rate = response.data.summary.rate;
        this.hzGetData.detail = response.data.detail
      }.bind(this))
      .catch(function(error){
        console.log(error);
      })
      .finally(function(){
        this.hzGetData.loading = false;        
      }.bind(this));
    },
    // HZ総拠点数
    calcHzAllGetData(){      
      this.hzAllData.loading = true;

      //let url = 'http://localhost:8080/cgi-bin/kpi_summary2.py';
      let url = 'server/cgi-bin/kpi_summary2.py';
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        console.log(response.data);
        this.hzAllData.all = response.data.summary.all;
        this.hzAllData.num = response.data.summary.num;
        this.hzAllData.rate = response.data.summary.rate;
        this.hzAllData.detail = response.data.detail
      }.bind(this))
      .catch(function(error){
        console.log(error);
      })
      .finally(function(){
        this.hzAllData.loading = false;        
      }.bind(this));
    },
    // 3.SD総拠点数
    calcSdAllGetData(){
      this.sdAllData.loading = true;

      //let url = 'http://localhost:8080/cgi-bin/kpi_summary3.py';
      let url = 'server/cgi-bin/kpi_summary3.py';
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        console.log('exec SD ALL!')
        console.log(response.data);
        this.sdAllData.all = response.data.summary.all;
        this.sdAllData.num = response.data.summary.num;
        this.sdAllData.rate = response.data.summary.rate;
        this.sdAllData.detail = response.data.detail
      }.bind(this))
      .catch(function(error){
        console.log(error);
      })
      .finally(function(){
        this.sdAllData.loading = false;        
      }.bind(this));
    },
    // 4.DP設置台数
    calcDpGetData(){
      this.dpData.loading = true;

      //let url = 'http://localhost:8080/cgi-bin/kpi_summary4.py';
      let url = 'server/cgi-bin/kpi_summary4.py';
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        console.log('exec Dp!')
        console.log(response.data);
        this.dpData.all = response.data.summary.all;
        this.dpData.num = response.data.summary.num;
        this.dpData.rate = response.data.summary.rate;
        this.dpData.detail = response.data.detail;
        console.log(this.dpData.detail);
      }.bind(this))
      .catch(function(error){
        console.log(error);
      })
      .finally(function(){
        this.dpData.loading = false;        
      }.bind(this));
    },
    // 5.大陳列
    calcDisplayGetData(){
      this.displayData.loading = true;

      //let url = 'http://localhost:8080/cgi-bin/kpi_summary5.py';
      let url = 'server/cgi-bin/kpi_summary5.py';
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        console.log('exec Display')
        console.log(response.data);
        this.displayData.all = response.data.summary.all;
        this.displayData.num = response.data.summary.num;
        this.displayData.rate = response.data.summary.rate;
        this.displayData.detail = response.data.detail;
      }.bind(this))
      .catch(function(error){
        console.log(error);
      })
      .finally(function(){
        this.displayData.loading = false;        
      }.bind(this));
    },
    // 6.インプロ金額
    calcInproGetData(){
      this.inproData.loading = true;

      //let url = 'http://localhost:8080/cgi-bin/kpi_summary6.py';
      let url = 'server/cgi-bin/kpi_summary6.py';
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        console.log('exec Inpro!')
        console.log(response.data);
        this.inproData.all = response.data.summary.all;
        this.inproData.num = response.data.summary.num;
        this.inproData.rate = response.data.summary.rate;
        this.inproData.detail = response.data.detail;
      }.bind(this))
      .catch(function(error){
        console.log(error);
      })
      .finally(function(){
        this.inproData.loading = false;        
      }.bind(this));
    },
  },
}
</script>
