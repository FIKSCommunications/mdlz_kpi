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
        >
        </summaryGraph>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <summaryGraph
        :title="inproData.title"
        :cols="inproData.cols"
        :all="inproData.all"
        :rate="inproData.rate"
        :num="inproData.num"
        regi="none"
        cavarege="none"
        >
        </summaryGraph>
      </v-col>
    </v-row>
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
      },
      hzAllData:{
        id:2,
        title:'②　HZ総拠点数',
        cols:['ターゲット','拠点数','達成率'],
        all :300,
        num  :300,
        rate:100,
      },
      sdAllData:{
        id:3,
        title:'③　SD総拠点数',
        cols:['ターゲット','拠点数','達成率'],
        all :300,
        num  :300,
        rate:86,
      },
      dpData:{
        id:4,
        title:'④　DP設置台数',
        cols:['ターゲット','設置台数','達成率'],
        all :300,
        num  :300,
        rate:130,
      },
      displayData:{
        id:5,
        title:'⑤　大陳列',
        cols:['ターゲット','大陳回数','達成率'],
        all :300,
        num  :300,
        rate:99,
      },
      inproData:{
        id:6,
        title:'⑥　インプロ金額',
        cols:['ターゲット','インプロ金額','達成率'],
        all :300,
        num  :300,
        rate:98,
      },
      startDt:moment(new Date).startOf("month").format('YYYY-MM'),
      endDt:moment(new Date).endOf("month").format('YYYY-MM'),
      viewFlgSummary:false,
    }
  },
  methods:{
    clickAggregate(){
      this.viewFlgSummary = true;
      this.calcHzGetData();
      this.calcHzAllGetData();
    },
    // HZ占有率
    calcHzGetData(){
      console.log('axios!')
      let url = 'http://localhost:8080/cgi-bin/kpi_summary1.py';
      const response = axios.get(url, {
        params: {
          'startdt': this.startDt,
          'enddt': this.endDt,
          'clientid': 162,
        }
      })
      .then(function(response){
        console.log('exec!')
        console.log(response.data);
        this.hzGetData.all = response.data.summary.all;
        this.hzGetData.regi = response.data.summary.regi;
        this.hzGetData.num = response.data.summary.num;
        this.hzGetData.cavarege = response.data.summary.cavarege;
        this.hzGetData.rate = response.data.summary.rate;
        this.hzGetData.detail = response.data.detail
      }.bind(this));
    },
    // HZ総拠点数
    calcHzAllGetData(){
      console.log('axios!')
      let url = 'http://localhost:8080/cgi-bin/kpi_summary2.py';
      const response = axios.get(url, {
        params: {
          'startdt': '2020-01-01',
          'enddt': '2020-01-31'
        }
      })
      .then(function(response){
        console.log('exec!')
        console.log(response.data);
        // this.hzAllData.all = response.data.regi;
        // this.hzAllData.num = response.data.kyoten;
        // this.hzAllData.rate = response.data.result;
      }.bind(this));
    },
    // SD総拠点数
    calcSdAllGetData(){
      console.log('axios!')
      let url = 'http://localhost:8080/cgi-bin/kpi_summary3.py';
      const response = axios.get(url, {
        params: {
          'startdt': '2020-01-01',
          'enddt': '2020-01-31'
        }
      })
      .then(function(response){
        console.log('exec!')
        console.log(response.data);
        this.sdAllData.all = response.data.regi;
        this.sdAllData.num = response.data.kyoten;
        this.sdAllData.rate = response.data.result;
      }.bind(this));
    },
    // DP設置台数
    calcDpGetData(){
      console.log('axios!')
      let url = 'http://localhost:8080/cgi-bin/kpi_summary4.py';
      const response = axios.get(url, {
        params: {
          'startdt': '2020-01-01',
          'enddt': '2020-01-31'
        }
      })
      .then(function(response){
        console.log('exec!')
        console.log(response.data);
        this.dpData.all = response.data.regi;
        this.dpData.num = response.data.kyoten;
        this.dpData.rate = response.data.result;
      }.bind(this));
    },
    // 大陳列
    calcDisplayGetData(){
      console.log('axios!')
      let url = 'http://localhost:8080/cgi-bin/kpi_summary4.py';
      const response = axios.get(url, {
        params: {
          'startdt': '2020-01-01',
          'enddt': '2020-01-31'
        }
      })
      .then(function(response){
        console.log('exec!')
        console.log(response.data);
        this.displayData.all = response.data.regi;
        this.displayData.num = response.data.kyoten;
        this.displayData.rate = response.data.result;
      }.bind(this));
    },
    // インプロ金額
    calcInproGetData(){
      console.log('axios!')
      let url = 'http://localhost:8080/cgi-bin/kpi_summary6.py';
      const response = axios.get(url, {
        params: {
          'startdt': '2020-01-01',
          'enddt': '2020-01-31'
        }
      })
      .then(function(response){
        console.log('exec!')
        console.log(response.data);
        this.inproData.all = response.data.regi;
        this.inproData.num = response.data.kyoten;
        this.inproData.rate = response.data.result;
      }.bind(this));
    },
  },
}
</script>
