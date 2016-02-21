// Vue.use(VueRouter);
Vue.use(VueResource);

Vue.http.options.root = '/api';

new Vue({
  el: '#app',
  data: {
    key: '',
    provider: '',
    region: '',
    vpns: Array.new,
    providers: Array.new,
    regions: Array.new
  },
  ready: function () {
    this.key = localStorage._key;
    this.provider = localStorage.provider;
    this.region = localStorage.region;

    if (this.key || this.provider || this.region) {
      this.remember = true;
    }

    this.$http.get('providers')
      .then(function (resp) {
        this.$set('providers', resp.data);
      }, function (resp) {
        console.log(resp);
      }
    );
  },
  methods: {

    getList: function () {
      this.$http.get('', { region: this.region, key: this.key, provider: this.provider })
        .then(function (resp) {
          this.$set('vpns', resp.data);
        }, function (resp) {
          console.log(resp);
        }
      );
    },

    create: function () {
      this.$http.post('', { region: this.region, key: this.key, provider: this.provider })
        .then(function (resp) {
          if (this.vpns === undefined) {
            this.vpns = [];
          }
          this.vpns.push(resp.data);
        }, function (resp) {
          console.log(resp);
        }
      );
    },

    delete: function (vpn) {
      this.$http.delete('', { vpn_id: vpn.id, key: this.key, provider: this.provider })
        .then(function (resp) {
          this.vpns.splice(this.vpns.indexOf(vpn), 1);
        }, function (resp) {
          console.log(resp);
        }
      );
    }
  },
  watch: {
    'provider': function (val, oldVal) {
        if (!this.key || !val) {
          return ;
        }
        this.$http.get('regions', { provider: this.provider, key: this.key })
        .then(function (resp) {
          this.$set('regions', resp.data);
          if (this.remember) {
              localStorage.provider = this.provider;
          }
        }, function (resp) {
          console.log(resp)
        }
      );
    },
    'key': function (val, oldVal) {
        if (!this.provider || !val) {
          return ;
        }
        this.$http.get('regions', { provider: this.provider, key: this.key })
        .then(function (resp) {
          this.$set('regions', resp.data);
          if (this.remember) {
              localStorage._key = this.key;
          }
        }, function (resp) {
          console.log(resp)
        }
      );
    },
    'region': function (val, oldVal) {
        if (this.remember) {
            localStorage.region, this.region;
        }
    },
    'remember': function (val, oldVal) {
        if (val) {
          localStorage.provider = this.provider;
          localStorage.region = this.region;
          localStorage._key = this.key;
        } else {
          localStorage.removeItem('provider');
          localStorage.removeItem('region');
          localStorage.removeItem('_key');
        }
    }
  }
})
