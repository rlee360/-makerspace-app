<template>
  <div class="container mt-5 mb-5">
    <h1>OPERATOR</h1>
    <div class="row">
      <div class="col mx-2 px-2 py-3 bg-light border rounded">
        <h6>New Jobs</h6>
        <draggable class="draggable-list" :list="incomplete_jobs" group="_jobs">
          <div v-for="job in incomplete_jobs" :key="job._id.$oid">
            <div class="bg-white mt-3 p-2 shadow border rounded">
              <p>{{ job.filename }}</p>
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
                  <p>{{ job.filename }}</p>
                </div>
              </div>
            </draggable>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="col mx-2 px-2 py-3 bg-light border rounded" style="max-height:300px">
          <h6>Completed</h6>
          <!--          <draggable class="draggable-list" :list="tasks.completed" group="tasks">-->
          <!--            <div v-for="(task, i) in tasks.completed" :key="i">-->
          <!--              <div class="bg-white mt-3 p-2 shadow border rounded">-->
          <!--                <p>{{ task.title }}</p>-->
          <!--              </div>-->
          <!--            </div>-->
          <!--          </draggable>-->
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
      completed_jobs: []
    };
  },
  async mounted() {
    let job_query = {};
    res = await axios.post("http://localhost:5000/api/request/filter", job_query, {'Content-Type': 'multipart/form-data'});
    this.jobs = res.data.filtered;
    let res = await axios.get("http://localhost:5000/api/machine/?maintenance=False");
    let m = res.data;
    for (const el of m) {
      res = await axios.get("http://localhost:5000/api/machine/?machine=" + el['_id']);
      this.machines.push(res.data[0]);
    }
    for (const mac of this.machines) {
      mac.jobs = this.jobs.filter((el) => el.machine === mac._id);
    }
  },
  computed: {
    incomplete_jobs() {
      return this.jobs.filter((el) => el.status === 'inactive');
    }
  },
  methods: {
    async modifyJob(evt, mid) {
      window.rr = evt;
      if (!evt.added) return;
      let req_data = {
        "id": evt.added.element._id.$oid,
        "machine": mid,
        "status": "queued"
      }
      const res = await axios.post("http://localhost:5000/api/request/update", req_data, {'Content-Type': 'application/json'});
      console.log(res);
      evt.added.element.status = 'queued';
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