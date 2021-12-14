<template>
  <div class="card text-center m-3">
    <h5 class="card-header">Job View</h5>
    <div style="width:70%;margin:auto">
      <model-stl backgroundColor="#fee"
                 :lights="model_lights"
                 :src="`http://localhost:5000/api/request/download/${job_data._id.$oid}`"></model-stl>
    </div>
    <div class="card-body">
      <pre>
      <b>Job ID:</b> {{ job_data._id.$oid }}
      <b>Status:</b> {{ job_data.status }}
      <b>Query Position:</b> {{ job_data.queue_position }}
      <b>Machine:</b> {{ job_data.machine }}
      <b>Filename:</b> {{ job_data.filename }}
      <b>Material:</b> {{ `${material_data.color} ${material_data.material} (${material_data.brand})` }}
      <b>Shells:</b> {{ job_data.shells }}
      <b>Infill:</b> {{ job_data.infill }}
      <b>Top and Bottom Layers:</b> {{ job_data.top_bottom }}
      <b>Email:</b> {{ JSON.stringify(job_data.email).slice(1, -1) }}
      <b>Submitted by:</b> {{ job_data.name }}
      <b>Class:</b> {{ job_data.class_id }}
      <b>Date:</b> {{ new Date(job_data.datetime.$date) }}
      </pre>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {ModelStl} from 'vue-3d-model';

export default {
  components: {ModelStl},
  data() {
    return {
      job_data: [],
      material_data: {},
      model_lights: [
          {
            type: 'HemisphereLight',
            position: { x: 0, y: 1, z: 0 },
            skyColor: 0xaaaaff,
            groundColor: 0x806060,
            intensity: 0.5,
          },
          {
            type: 'DirectionalLight',
            position: { x: 1, y: -1, z: 1 },
            color: 0xffffff,
            intensity: 0.8,
          },
      ]
    }
  },
  methods: {
    async created() {
      const response = await axios.get("http://localhost:5000/api/request/status/" + new URL(location.href).searchParams.get('id'));
      this.job_data = response.data;
      window.dd = this.job_data;

      const res = await axios.get("http://localhost:5000/api/material/view/" + this.job_data.material);
      this.material_data = res.data;
      window.dd = this.material_data;
    }
  },

  async mounted() {
    const response = await axios.get("http://localhost:5000/api/request/status/" + new URL(location.href).searchParams.get('id'));
    this.job_data = response.data;
    window.dd = this.job_data;

    const res = await axios.get("http://localhost:5000/api/material/view/" + this.job_data.material);
    this.material_data = res.data;
    window.dd = this.material_data;
  },
}
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';

</style>