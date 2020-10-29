<template>
  <div class="optimize">
    <page-header> </page-header>
      <v-container grid-list-xl class="text-md-center" style="min-width:100%">
        <h2> FERTILIZER SELECTION </h2>

          <v-dialog v-model="fertilizer_dialog" persistent max-width="1000px">
            <v-card>
              <v-card-title>
                <span class="headline">Add Fertilizer</span>
              </v-card-title>
              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>

                    <v-flex xs12 sm6 md4>
                      <v-text-field label="Fertilizer name" v-model="fertilizer_add_Item.fertilizer_name" required></v-text-field>
                    </v-flex>

                    <v-flex xs12 sm6 md4>
                      <v-text-field label="Cost per kg (INR)" hint="Per kg cost of the fertilizer" v-model="fertilizer_add_Item.cost_per_kg" required></v-text-field>
                    </v-flex>

                    <v-flex xs12 sm6 md4>
                      <v-text-field label="Quantity of fertilizer in one bag (kg)" v-model="fertilizer_add_Item.unit_in_kg" required></v-text-field>
                    </v-flex>

                    <v-flex xs12 sm6 md4>
                      <v-text-field label="Quantity of Nitrogen per bag (kg)" v-model="fertilizer_add_Item.n_per_unit" required></v-text-field>
                    </v-flex>

                    <v-flex xs12 sm6 md4>
                      <v-text-field label="Quantity of Phosphorus per bag (kg)" v-model="fertilizer_add_Item.p_per_unit" required></v-text-field>
                    </v-flex>

                    <v-flex xs12 sm6 md4>
                      <v-text-field label="Quantity of Potassium per bag (kg)" v-model="fertilizer_add_Item.k_per_unit"  required></v-text-field>
                    </v-flex>

                    <v-flex xs12 sm6 md4>
                      <v-text-field label="Quantity of Sulphur per bag (kg)" v-model="fertilizer_add_Item.s_per_unit"  required></v-text-field>
                    </v-flex>

                  </v-layout>
                </v-container>
                <small>*indicates required field</small>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click.native="fertilizer_add_close">Close</v-btn>
                <v-btn color="blue darken-1" flat @click.native="fertilizer_add_save">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <!-- Dialog box to edit fertilizer bag cost -->

          <v-dialog v-model="dialog" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>
                    <v-flex xs12 sm6 md4>
                      <v-text-field :readonly=true v-model="editedItem.fertilizer_name" label="Fertilizer name"></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6 md4>
                      <v-text-field :readonly=true v-model="editedItem.unit_in_kg" label="Weight of the bag (kg)"></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6 md4>
                      <v-text-field v-model="editedItem.bag_cost" label="Cost of the bag (INR)"></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" flat @click.native="close">Cancel</v-btn>
                <v-btn color="primary" flat @click.native="save">Save</v-btn>
              </v-card-actions>

            </v-card>
          </v-dialog>

          <!-- Section to select the fertilizers as per need -->

          <v-btn round class="mx-0" @click="add_fertilizer"> Add new Fertilizer </v-btn>
          <v-btn round class="mx-0" @click="refresh"> Refresh Fertilizer list </v-btn>

          <v-data-table :rows-per-page-items=[25] :headers="headers" :items="fertilizer_list" :search="search"
          v-model="selected_fertilizer" item-key="fertilizer_name" select-all class="elevation-1">

            <template slot="headerCell" slot-scope="props">
              <v-tooltip bottom>
                <span slot="activator"> {{ props.header.text }} </span>
                <span> {{ props.header.text }} </span>
              </v-tooltip>
            </template>

            <template slot="items" slot-scope="props">
              <td> <v-checkbox v-model="props.selected" primary hide-details></v-checkbox> </td>
              <td class="justify-center">{{ props.item.fertilizer_name }}</td>
              <td class="justify-center">{{ props.item.unit_in_kg }}</td>
              <td class="justify-center">{{ props.item.bag_cost }}</td>
              <td class="justify-center layout px-0">
                <v-btn icon class="mx-0" @click="editItem(props.item)">
                  <v-icon color="primary">edit</v-icon>
                </v-btn>
                <v-btn icon class="mx-0" @click="deleteItem(props.item)">
                  <v-icon color="primary">delete</v-icon>
                </v-btn>
              </td>
            </template>
          </v-data-table>
          <br>
       <a href="#fertilizer-dtl-section">
       <v-btn round class="mx-0" @click="optimize"> Submit Fertilizer </v-btn>
     </a>

       <h2> FERTILIZER OPTIMIZER </h2>

       <!-- Section to display the N,P,K and cost for optimial fertilizer combination  -->

       <div id="fertilizer-dtl-section">
         <v-btn round class="mx-0" @click="display_result">
           <v-icon color="primary">show_chart</v-icon>  Run Fertilizer Optimizer
         </v-btn>
         <br>
         <br>

         <p> The fertilizer application recommended vary in the range +/- 20 kgs from the deficit N,P,K calculated </p>

         <v-layout>
           <v-text-field :readonly=true v-model="NPK_deficit.N_deficit" label="Deficit Nitrogen (kg)" style="width:50px"></v-text-field>
           <v-text-field :readonly=true v-model="optimized_output.optimized_N_qty" label="Estimated Nitrogen (kg)" style="width:50px"></v-text-field>
         </v-layout>

         <v-layout>
           <v-text-field :readonly=true v-model="NPK_deficit.P_deficit" label="Deficit Phosphorus (kg)" style="width:50px"></v-text-field>
           <v-text-field :readonly=true v-model="optimized_output.optimized_P_qty" label="Estimated Phosphorus (kg)" style="width:50px"></v-text-field>
         </v-layout>

         <v-layout>
           <v-text-field :readonly=true v-model="NPK_deficit.K_deficit" label="Deficit Potassium (kg)" style="width:50px"></v-text-field>
           <v-text-field :readonly=true v-model="optimized_output.optimized_K_qty" label="Estimated Potassium (kg)" style="width:50px"></v-text-field>
         </v-layout>

         <v-layout>
           <v-text-field :readonly=true v-model="optimized_output.total_cost" align="center" label="Total Cost (INR)" style="width:50px"></v-text-field>
         </v-layout>

       </div>

       <h3> FERTILIZER SUGGESTION </h3>

       <!-- Section to display the optimial fertilizer combination  -->

       <v-data-table :headers="optimized_headers" :items="optimized_fertilizer_list" hide-actions class="elevation-1">
         <template slot="items" slot-scope="props">
           <td class="justify-center">{{ props.item.fertilizer_name }}</td>
           <td class="justify-center">{{ props.item.fertilizer_bag_required }}</td>
           <td class="justify-center">{{ props.item.fertilizer_bag_weight }}</td>
         </template>
       </v-data-table>

       <v-btn  round color="primary" :to="{'name':'Home'}">
         New query
       </v-btn>
     </v-container>
     <br>

     <div class="page-footer">
       This app has been developed as a part of "A Model of Comprehensive Agribusiness Extension Service in Karnataka (CABES)", Department of Agriculture, Government of Karnataka
   </div>

   </div>
</template>

<script>
import API from '../reducers/API'
import _ from 'lodash';

  export default {
    name: 'FertilizerOptimizer',
    data () {
      return {
        fertilizer_list:[],
        optimized_headers: [
          { text: 'Fertilizer name',align: 'center',sortable: false,value: 'fertilizer_name'},
          { text: 'Number of bags required', value: 'fertilizer_bag_required',align:'center'},
          { text: 'Weight of the fertilizer bag (kg)', value: 'fertilizer_bag_weight',align:'center'}
        ],
        NPK_deficit:{
          N_deficit:0,
          P_deficit:0,
          K_deficit:0
        },
        search:'',
        selected_fertilizer:[],
        optimized_output:{},
        optimized_fertilizer_list :[],
        dialog: false,
        headers: [
          { text: 'Fertilizer name',align: 'center',sortable: false,value: 'fertilizer_name',textcolor:"primary"},
          { text: 'Weight of the bag (kg)', align: 'center', value: 'unit_in_kg' },
          { text: 'Cost of the bag (INR)', align: 'center',sortable: true, value: 'bag_cost' },
          { text: 'Actions', value: 'name', align: 'center', sortable: false }
        ],
        editedIndex: -1,
        editedItem: {
          fertilizer_name: '',
          unit_in_kg: 0,
          bag_cost: 0
        },
        defaultItem: {
          fertilizer_name: '',
          unit_in_kg: 0,
          bag_cost: 0
        },
        fertilizer_dialog:false,
        fertilizer_add_Item: {
          fertilizer_name: '',
          cost_per_kg:0,
          unit_in_kg: 0,
          n_per_unit:0,
          p_per_unit:0,
          k_per_unit:0,
          s_per_unit:0
        }
        }
      },

    created : function () {
      this.NPK_deficit = this.$store.selects.NPK_deficit
      this.load()
      },

      mounted : function () {
        this.selected_fertilizer = []
        this.optimized_output = {}
        this.optimized_fertilizer_list = []
        this.NPK_deficit = this.$store.selects.NPK_deficit
      },

      methods:{
        load(){
          API.fetchFertilizerData()
          .then(fertilizer_info => {
            this.fertilizer_list = fertilizer_info.fertilizer
          })
          .catch(error => {
          console.error(error);
        })
        },
        add_fertilizer(){
          var alert_message = ''
          this.fertilizer_dialog = true;
        },
        refresh(){
          this.load()
        },
        editItem (item) {
          this.editedIndex = this.fertilizer_list.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialog = true
        },

        deleteItem (item) {
          const index = this.fertilizer_list.indexOf(item)
          confirm('Are you sure you want to delete this item?') && this.fertilizer_list.splice(index, 1)
        },
        close () {
          this.dialog = false
          setTimeout(() => {
            this.editedItem = Object.assign({}, this.defaultItem)
            this.editedIndex = -1
          }, 300)
        },

        save () {
          if (this.editedIndex > -1) {
            Object.assign(this.fertilizer_list[this.editedIndex], this.editedItem)
          } else {
            this.fertilizer_list.push(this.editedItem)
          }
          this.close()
        },
        fertilizer_add_close () {
          this.fertilizer_dialog = false
          // console.log("I am in fertilizer close section")
        },
        fertilizer_add_save () {
          var alert_message = ''
          // console.log("I am in fertilizer save section")
          // console.log(this.fertilizer_add_Item)
          API.AddFertilizerData(this.fertilizer_add_Item)
              .then(response_out => {
                alert(response_out) })
              .catch(error => {
                console.log(error);
              })
          this.fertilizer_add_close()
          this.load()
        },
      optimize(){
        this.optimized_fertilizer_list = []
        var fertilizer_name_list  = _.map(this.selected_fertilizer, 'fertilizer_name');
        var fertilizer_bag_cost_list  = _.map(this.selected_fertilizer, 'bag_cost');
        var args = {	"opts":"single",
                  "N_deficit": this.$store.selects.NPK_deficit.N_deficit,
                  "P_deficit": this.$store.selects.NPK_deficit.P_deficit,
                  "K_deficit": this.$store.selects.NPK_deficit.K_deficit,
                  "fertilizer_name": fertilizer_name_list,
                  "fertilizer_bag_cost": fertilizer_bag_cost_list
                }
        this.$store.api.optimized_output = {}

        API.fetchOptimizedData(args)
            .then(optimized_response => {
              this.$store.api.optimized_output = optimized_response.optimized_output})
            .catch(error => {
              console.log(error);
            })

        },

      display_result(){
        this.optimized_output = this.$store.api.optimized_output
        var s = this.optimized_output.fertilizer_name
        for (var i=0;i < this.optimized_output.fertilizer_name.length; i++){
          if(this.optimized_output.fertilizer_bag_required[i]!=0){
            this.optimized_fertilizer_list.push({"fertilizer_name": this.optimized_output.fertilizer_name[i],
                              "fertilizer_bag_required": this.optimized_output.fertilizer_bag_required[i],
                              "fertilizer_bag_weight": this.optimized_output.fertilizer_bag_weight[i]})
                            }
            }

      }
      },

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        }
      },

      watch:{
        dialog (val) {
          val || this.close()
        },
        fertilizer_dialog (val) {
          val || this.fertilizer_add_close()
        }
      },

  }

</script>

<style scoped>

  @import '../stylesheet/stylesheet.css'

</style>
