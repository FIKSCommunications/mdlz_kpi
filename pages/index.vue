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
        <v-card>
          <v-card-title>
            ①　HZ占有率
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-simple-table dense>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left">
                          レジ台数
                        </th>
                        <th class="text-left">
                          所有率
                        </th>
                        <th class="text-left">
                          カバレッジ
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{{ hzGetData.all }}</td>
                        <td>{{ hzGetData.rate }}</td>
                        <td>{{ hzGetData.num }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-col>
              <v-col class=mt-3>
                <v-progress-linear
                  :value="hzGetData.rate"
                  :color="hzGetData.rate == 100 ? 'green' : 'warning' "
                  height="20"
                >
                  <strong>{{hzGetData.rate}}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <v-card>
          <v-card-title>
            ②　HZ総拠点数
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-simple-table dense>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left">
                          レジ台数
                        </th>
                        <th class="text-left">
                          所有率
                        </th>
                        <th class="text-left">
                          カバレッジ
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{{ hzAllData.all }}</td>
                        <td>{{ hzAllData.rate }}</td>
                        <td>{{ hzAllData.num }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-col>
              <v-col class=mt-3>
                <v-progress-linear
                  :value="hzAllData.rate"
                  :color="hzAllData.rate == 100 ? 'green' : 'warning' "
                  height="20"
                >
                  <strong>{{hzAllData.rate}}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <v-card>
          <v-card-title>
            ③　SD総拠点数
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-simple-table dense>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left">
                          レジ台数
                        </th>
                        <th class="text-left">
                          所有率
                        </th>
                        <th class="text-left">
                          カバレッジ
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{{ sdAllData.all }}</td>
                        <td>{{ sdAllData.rate }}</td>
                        <td>{{ sdAllData.num }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-col>
              <v-col class=mt-3>
                <v-progress-linear
                  :value="sdAllData.rate"
                  :color="sdAllData.rate == 100 ? 'green' : 'warning' "
                  height="20"
                >
                  <strong>{{sdAllData.rate}}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <v-card>
          <v-card-title>
            ④　DP設置台数
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-simple-table dense>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left">
                          レジ台数
                        </th>
                        <th class="text-left">
                          所有率
                        </th>
                        <th class="text-left">
                          カバレッジ
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{{ dpData.all }}</td>
                        <td>{{ dpData.rate }}</td>
                        <td>{{ dpData.num }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-col>
              <v-col class=mt-3>
                <v-progress-linear
                  :value="dpData.rate"
                  :color="dpData.rate == 100 ? 'green' : 'warning' "
                  height="20"
                >
                  <strong>{{dpData.rate}}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  <v-row justify="center" align="center" v-show="viewFlgSummary">
        <v-col cols="8">
          <v-card>
            <v-card-title>
              ⑥　インプロ金額
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="6">
                  <v-simple-table dense>
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-left">
                            レジ台数
                          </th>
                          <th class="text-left">
                            所有率
                          </th>
                          <th class="text-left">
                            カバレッジ
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>{{ displayData.all }}</td>
                          <td>{{ displayData.rate }}</td>
                          <td>{{ displayData.num }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-col>
                <v-col class=mt-3>
                  <v-progress-linear
                    :value="displayData.rate"
                    :color="displayData.rate == 100 ? 'green' : 'warning' "
                    height="20"
                  >
                  <strong>{{displayData.rate}}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-show="viewFlgSummary">
      <v-col cols="8">
        <v-card>
          <v-card-title>
            ⑤　大陳列
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-simple-table dense>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left">
                          レジ台数
                        </th>
                        <th class="text-left">
                          所有率
                        </th>
                        <th class="text-left">
                          カバレッジ
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{{ inproData.all }}</td>
                        <td>{{ inproData.rate }}</td>
                        <td>{{ inproData.num }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-col>
              <v-col class=mt-3>
                <v-progress-linear
                  :value="inproData.rate"
                  :color="inproData.rate == 100 ? 'green' : 'warning' "
                  height="20"
                >
                  <strong>{{inproData.rate}}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import moment from "moment";
export default {

  data () {
    return {
      hzGetData:{
        all :300,
        rate:80,
        num  :300,
      },
      hzAllData:{
        all :300,
        rate:100,
        num  :300,
      },
      sdAllData:{
        all :300,
        rate:86,
        num  :300,
      },
      dpData:{
        all :300,
        rate:67,
        num  :300,
      },
      displayData:{
        all :300,
        rate:70,
        num  :300,
      },
      inproData:{
        all :300,
        rate:98,
        num  :300,
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
