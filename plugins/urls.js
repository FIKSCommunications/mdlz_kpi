import Vue from 'vue'

Vue.prototype.$urls = {
    envFlg:'pro',  // dev or pro
    devPythonUrl: 'http://localhost:8080/cgi-bin',
    proPythonUrl: 'server/cgi-bin',
}