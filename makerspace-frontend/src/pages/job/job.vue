<template>
  <div class="card text-center m-3">
    <h5 class="card-header">Job View</h5>
    <div class="card-body">
      <pre>
      <b>Job ID:</b> {{job_data._id.$oid}}
      <b>Status:</b> {{job_data.status}}
      <b>Query Position:</b> {{job_data.queue_position}}
      <b>Machine:</b> {{job_data.machine}}
      <b>Filename:</b> {{job_data.filename}}
      <b>Material:</b> {{`${material_data.color} ${material_data.material} (${material_data.brand})` }}
      <b>Shells:</b> {{job_data.shells}}
      <b>Infill:</b> {{job_data.infill}}
      <b>Top Bottom:</b> {{job_data.top_bottom}}
      <b>Email:</b> {{job_data.email}}
      <b>Submitted by:</b> {{job_data.name}}
      <b>Class:</b> {{job_data.class_id}}
      </pre>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      job_data:[],
      material_data:{}
    }
  },
  methods:{
  async created() {
    const response = await axios.get("http://localhost:5000/api/request/status/"+ new URL(location.href).searchParams.get('id'));
    this.job_data = response.data;
    window.dd = this.job_data;

    const res = await axios.get("http://localhost:5000/api/material/view/"+ this.job_data.material);
    this.material_data = res.data;
    window.dd = this.material_data;
  }
  },

  async mounted() {
    const response = await axios.get("http://localhost:5000/api/request/status/"+ new URL(location.href).searchParams.get('id'));
    this.job_data = response.data;
    window.dd = this.job_data;

    const res = await axios.get("http://localhost:5000/api/material/view/"+ this.job_data.material);
    this.material_data = res.data;
    window.dd = this.material_data;
  },
}
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';
</style>