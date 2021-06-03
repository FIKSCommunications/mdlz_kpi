<template>
      <v-select
        v-model="selectedOptions"
        :items="filteredData"
        :label="label"
        @change="updateValue"
        multiple
      >
        <template v-slot:prepend-item>
          <v-list-item>
            <v-text-field
              v-model="filterString"
              label=""
              placeholder="検索..."
              prepend-inner-icon="mdi-search"
              outlined
              clearable
              dense
              hide-details
            ></v-text-field>
          </v-list-item>

          <v-list-item
            @click="toggle"
          >
            <v-list-item-action class="mt-0 mb-0">
              <v-icon :color="selectedOptions.length > 0 ? 'indigo darken-4' : ''">{{ icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>すべて選択</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-divider class="m-0"></v-divider>
        </template>
      </v-select>
</template>

<style>
.v-list-item__action {
  margin: 0;
}
</style>

<script>
export default {
  props:[
      "label",
      "listOptions",
  ],
  data: () => ({
    filterString:"",
    Options: [],
    selectedOptions: [],
  }),
  computed: {
    likesAllOption () {
      return this.selectedOptions.length === this.Options.length
    },
    likesSomeOption () {
      return this.selectedOptions.length > 0 && !this.likesAllOption
    },
    icon () {
      if (this.likesAllOption) return 'mdi-close-box'
      if (this.likesSomeOption) return 'mdi-minus-box'
      return 'mdi-checkbox-blank-outline'
    },
    //フィルター
    filteredData() {
        if (this.filterString === "") return this.Options;
        return this.Options.filter(item => item.indexOf(this.filterString) !== -1)
    },
  },

  created () {
    this.Options = this.listOptions;
  },

  watch: {
    listOptions (newData) {
      this.Options = newData;
    }
  },

  methods: {
    toggle () {
      this.$nextTick(() => {
        if (this.likesAllOption) {
          this.selectedOptions = []
        } else {
          this.selectedOptions = this.Options.slice()
        }
        this.updateValue();
      })
    },
    updateValue() {
      let value = this.selectedOptions.length ? this.selectedOptions : null
      this.$emit('input', value)
      this.$emit('selected', value)
    },
  }
}
</script>