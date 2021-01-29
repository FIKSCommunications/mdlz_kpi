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
                  type="date"
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols=5>
                <v-text-field
                  v-model="endDt"
                  label="終了日"
                  outlined
                  type="date"
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
        >
        </summaryGraph>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import moment from "moment";
import summaryGraph from "../components/summaryGraph";
export default {
  components:{
    summaryGraph,
  },
  data () {
    return {
      hzGetData:{
        title:'①　HZ占有率',
        cols:['レジ台数','占有率','カバレッジ'],
        all :300,
        num  :300,
        getRate:100,
        cavarege:100,
        rate:80,
      },
      hzAllData:{
        title:'②　HZ総拠点数',
        cols:['ターゲット','拠点数','達成率'],
        all :300,
        num  :300,
        rate:100,
      },
      sdAllData:{
        title:'③　SD総拠点数',
        cols:['ターゲット','拠点数','達成率'],
        all :300,
        num  :300,
        rate:86,
      },
      dpData:{
        title:'④　DP設置台数',
        cols:['ターゲット','設置台数','達成率'],
        all :300,
        num  :300,
        rate:130,
      },
      displayData:{
        title:'⑤　大陳列',
        cols:['ターゲット','大陳回数','達成率'],
        all :300,
        num  :300,
        rate:99,
      },
      inproData:{
        title:'⑥　インプロ金額',
        cols:['ターゲット','インプロ金額','達成率'],
        all :300,
        num  :300,
        rate:98,
      },
      startDt:moment(new Date).startOf("month").format('YYYY-MM-DD'),
      endDt:moment(new Date).endOf("month").format('YYYY-MM-DD'),
      viewFlgSummary:false,
    }
  },
  methods:{
    clickAggregate(){
      this.viewFlgSummary = true;
    },

  },
}
</script>
