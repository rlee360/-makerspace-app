<template>
  <div class="container mt-5 mb-5">
    <h1>OPERATOR</h1>
    <div class="row">
      <div class="col mx-2 px-2 py-3 bg-light border rounded">
        <h6>New Jobs</h6>
        <draggable class="draggable-list" :list="incomplete_jobs" group="_jobs">
          <div v-for="job in incomplete_jobs" :key="job._id.$oid">
            <div class="bg-white mt-3 p-2 shadow border rounded">
              <a :href="`//localhost:5000/api/request/download/${job._id.$oid}`">{{ job.filename }}</a>
              <br>
              <b>Material:</b> {{ job.material_str }}
            </div>
          </div>
        </draggable>
      </div>
      <div class="col">
        <div v-for="(mac, i) in machines" :key="i">
          <div class="col mx-2 px-2 py-3 bg-light border rounded" style="max-height:20vh">
            <h6>{{ mac._id }}</h6>
            <draggable class="draggable-list" :list="mac.jobs" group="_jobs" @change="(e) => modifyJob(e, mac._id)">
              <div v-for="job in mac.jobs" :key="job._id.$oid">
                <div class="bg-white mt-3 p-2 shadow border rounded">
                  <a :href="`//localhost:5000/api/request/download/${job._id.$oid}`">{{ job.filename }}</a>
                  <br>
                  <b>Material:</b> {{ job.material_str }}
                </div>
              </div>
            </draggable>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="col mx-2 px-2 py-3 bg-light border rounded">
          <h6>Completed</h6>
          <draggable class="draggable-list" :list="completed_jobs" group="_jobs" @change="completed">
            <div v-for="job in completed_jobs" :key="job._id.$oid">
              <div class="bg-white mt-3 p-2 shadow border rounded">
                <a :href="`//localhost:5000/api/request/download/${job._id.$oid}`">{{ job.filename }}</a>
                <br>
                <b>Material:</b> {{ job.material_str }}
              </div>
            </div>
          </draggable>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import axios from "axios";

export default {
  components: {
    draggable,
  },
  data() {
    return {
      jobs: [],
      machines: [],
      materials: []
    };
  },
  async mounted() {
    let job_query = {};
    res = await axios.post("http://localhost:5000/api/request/filter", job_query, {'Content-Type': 'multipart/form-data'});
    let jr = res.data.filtered;
    window.jr = jr;
    for (const el of jr) {
      if (!el.material) continue;
      res = await axios.get("http://localhost:5000/api/material/view/" + el['material']);
      el['material_str'] = `${res.data['color']} ${res.data['material']} (${res.data['brand']})`;
      el['material'] = res.data;
      this.jobs.push(el);
    }
    let res = await axios.get("http://localhost:5000/api/machine/?maintenance=False");
    let m = res.data;
    for (const el of m) {
      res = await axios.get("http://localhost:5000/api/machine/?machine=" + el['_id']);
      this.machines.push(res.data[0]);
    }
    for (const mac of this.machines) {
      mac.jobs = this.jobs.filter((el) => el.machine === mac._id && el.status === 'queued').sort((el1, el2) => el1.datetime - el2.datetime);
    }
  },
  computed: {
    incomplete_jobs() {
      return this.jobs.filter((el) => el.status === 'inactive').sort((el1, el2) => el2.datetime - el1.datetime);
    },
    completed_jobs() {
      return this.jobs.filter((el) => el.status === 'completed').sort((el1, el2) => el2.datetime - el1.datetime);
    }
  },
  methods: {
    async modifyJob(evt, mid) {
      if (!evt.added) return;
      window.a = this.machines;
      window.aa = evt.added;
      window.aaa = mid;
      if(!evt.added.element.material.valid_machines.includes(mid)) {
        //window.location.reload();
        let machine = this.machines.find(m => m._id === mid)
        machine.jobs = machine.jobs.filter(a => a._id.$oid !== evt.added.element._id.$oid);
        this.incomplete_jobs.push(evt.added.element);
        //window.location.href = '/operator';
        return;
      }
      let req_data = {
        "id": evt.added.element._id.$oid,
        "machine": mid,
        "status": "queued"
      }
      const res = await axios.post("http://localhost:5000/api/request/update", req_data, {'Content-Type': 'application/json'});
      console.log(res);
      evt.added.element.status = 'queued';
    },
    async completed(evt) {
      if (!evt.added) return;
      let req_data = {
        "id": evt.added.element._id.$oid,
        "status": "completed"
      }
      await axios.post("http://localhost:5000/api/request/update", req_data, {'Content-Type': 'application/json'});
      evt.added.element.status = 'completed';
    }
  }
};
</script>

<style scoped>
h6 {
  font-weight: 700;
}

.col {
  height: 90vh;
  overflow: auto;
}

.draggable-list {
  min-height: 10vh;
}

.draggable-list > div {
  cursor: pointer;
}
</style>