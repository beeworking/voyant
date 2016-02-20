// Vue.use(VueRouter);
Vue.use(VueResource);

Vue.http.options.root = '/api';

new Vue({
  el: '#app',
  data: {
    key: '',
    provider: 'digitalocean',
    region: 'AMS2',
    vpns: Array.new
  },
  methods: {

    getList: function () {
      this.$http.get('', { region: this.region, key: this.key, provider: this.provider })
        .then(function(resp) {
          this.$set('vpns', resp.data);
        }, function (resp) {
          console.log(resp);
        }
      );
    },

    create: function () {
      this.$http.post('', { region: this.region, key: this.key, provider: this.provider })
        .then(function(resp) {
          this.vpns.push(resp.data);
        }, function (resp) {
          console.log(resp);
        }
      );
    },

    delete: function(vpn) {
      this.$http.delete('', {vpn_id: vpn.id, key: this.key, provider: this.provider })
        .then(function(resp) {
          this.vpns.splice(this.vpns.indexOf(vpn), 1);
        }, function (resp) {
          console.log(resp);
        }
      );
    }
  }
})
