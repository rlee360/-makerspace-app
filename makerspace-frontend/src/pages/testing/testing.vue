<template>
  <!-- some code condensed for display reasons -->
  <FormulateForm v-model="values" @submit="submitHandler">
    <h2>Frosty's Frozen Treats</h2>
    <FormulateInput
      type="group"
      name="flavors"
      label="Create your custom order"
      help="Choose your hand-packed pints whipped up by our expert servers"
      add-label="+ Add Flavor"
      validation="required"
      :repeatable="true"
    >
      <div class="order">
        <FormulateInput name="flavor" type="select" label="Flavor" validation="required" :options="{ vanilla: 'Vanilla', chocolate: 'Chocolate', strawberry: 'Strawberry', pineapple: 'Pineapple'}" />
        <FormulateInput name="quantity" label="Quantity" type="number" min="1" validation="required|min:1" />
      </div>
    </FormulateInput>

    <FormulateInput name="deliveryMethod" type="radio" label="Delivery Method" validation="required" :options="{ local: 'Local Pick-up', delivery: 'Delivery (5-mile radius)' }" />
    <FormulateInput name="orderNotes" type="textarea" label="Order Notes" help="Allergies? Delivery instructions? Don't need the spoons? Let us know!" />
    <FormulateInput type="submit" value="Place Order" />
    <pre>{{ values }}</pre>
  </FormulateForm>
</template>

<script>
export default { data () { return { values: {} } }, methods: {submitHandler () { alert(`Thank you for your order!`) } } }
</script>