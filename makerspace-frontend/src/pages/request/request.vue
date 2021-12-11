<template>
  <div class="container mt-5 mb-5">
    <h1>REQUEST</h1>
    <b-button>Push Me</b-button>
    <div class="row">
      <div class="col mx-2 px-2 py-3 bg-light border rounded">
        <h6>New Jobs</h6>
        <draggable class="draggable-list" :list="tasks.jobs" group="tasks">
          <div v-for="(job, i) in tasks.jobs" :key="i">
            <div class="bg-white mt-3 p-2 shadow border rounded">
              <p>{{ job }}</p>
            </div>
          </div>
        </draggable>
      </div>
      <div class="col">
        <div class="col mx-2 px-2 py-3 bg-light border rounded">
          <h6>Printer 1</h6>
          <draggable class="draggable-list" :list="tasks.printer1" group="tasks">
            <div v-for="(job, i) in tasks.printer1" :key="i">
              <div class="bg-white mt-3 p-2 shadow border rounded">
                <p>{{ job }}</p>
              </div>
            </div>
          </draggable>
        </div>
        <div class="col mx-2 px-2 py-3 bg-light border rounded">
          <h6>Printer 2</h6>
          <draggable class="draggable-list" :list="tasks.printer2" group="tasks">
            <div v-for="(job, i) in tasks.printer2" :key="i">
              <div class="bg-white mt-3 p-2 shadow border rounded">
                <p>{{ job }}</p>
              </div>
            </div>
          </draggable>
        </div>
      </div>
      <div class="col">
        <div class="col mx-2 px-2 py-3 bg-light border rounded">
          <h6>Completed</h6>
          <draggable class="draggable-list" :list="tasks.completed" group="tasks">
            <div v-for="(task, i) in tasks.completed" :key="i">
              <div class="bg-white mt-3 p-2 shadow border rounded">
                <p>{{ task }}</p>
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
import {Axios} from "axios";
export default {
  components: {
    draggable,
  },
  data() {
    return {
      tasks: {
        jobs: [ ],
        printer1: ["iris1.stl", "gyroid_dissected1.stl"],
        printer2: ["aerospike_nozzle.stl", "brain_model.stl"],
        completed: [ ],
      },
      methods: {
        onSubmit(event) {
          // make a axios request
          console.log("Submit button pressed!");
        }
      }
    };
  },
  async mounted() {
    const res = await Axios.get("https://localhost:5000/api/get_filament");
    console.log("Hello, My Linh");
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