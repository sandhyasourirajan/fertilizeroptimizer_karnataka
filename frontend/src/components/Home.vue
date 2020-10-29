<template>
    <div class="home">
      <page-header> </page-header>
        <h2 class="text-md-center"> INPUT SECTION </h2>
          <div class="input-section">

            <v-layout row>
            <v-flex md6>
              <v-select name="sel1" :items="crop_select" :rules="[() => !!selected_crop || 'This field is required']" v-model="selected_crop" label="Select a crop" required></v-select>
              Selected crop is <span  class="highlight-input">  {{selected_crop}} </span>
            </v-flex>

            <v-flex md6>
              <v-select :items="irrigation_type_select" :rules="[() => !!selected_irrigation_type || 'This field is required']" v-model="selected_irrigation_type" label="Select an irrigation type code" required></v-select>
              Selected irrigation type code is <span  class="highlight-input">  {{selected_irrigation_type}} </span>
            </v-flex>
            </v-layout>

            <v-layout row>
            <v-flex md5>
              <v-text-field v-model.number="area_hectare" label="Enter the area of the land (in hectares)" v-on:keyup="fertilizer_calc()"></v-text-field>
              Area of land entered by you is <span  class="highlight-input"> {{area_hectare}} hectare(s) </span> </p>
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex md12>
              <p> Enter the soil test results
                Nitrogen   (N): <input id="NPK_soil_test_result.N_soil_test_result" type="number" placeholder="0" v-model="NPK_soil_test_result.N_soil_test_result" v-on:keyup="update_N_deficit" style="width:50px"/> kg/ha &nbsp
                Phosphorus (P): <input id="NPK_soil_test_result.P_soil_test_result" type="number" placeholder="0" v-model="NPK_soil_test_result.P_soil_test_result" v-on:keyup="update_P_deficit" style="width:50px"/> kg/ha &nbsp
                Potassium  (K): <input id="NPK_soil_test_result.K_soil_test_result" type="number" placeholder="0" v-model="NPK_soil_test_result.K_soil_test_result" v-on:keyup="update_K_deficit" style="width:50px"/> kg/ha </p>

              <div class="text-md-center">
                  <!-- <a href="#pie-chart-2"> -->
                    <v-btn round justify-center color="primary" @click.native="generate_deficit_chart()"><v-icon> pie_chart </v-icon>   Generate N,P,K statistics </v-btn>
                  <!-- </a> -->
              </div>
            </v-flex>
            </v-layout>
            <br>
          </div>

        <h2 class="text-md-center"> N,P,K CALCULATION </h2>

        <div class="n-p-k-calc-section">
              <br> <p> Fertilizer requirement for crop/irrigation type selected per hectare
              N: <span  class="highlight-input"> {{ NPK_per_hectare.N_per_hectare  }} </span> &nbsp kg/ha &nbsp &nbsp
              P: <span  class="highlight-input"> {{ NPK_per_hectare.P_per_hectare }} </span> &nbsp kg/ha &nbsp &nbsp
              K: <span  class="highlight-input"> {{ NPK_per_hectare.K_per_hectare }} </span> &nbsp kg/ha
              </p>

              <v-layout row wrap >
                <v-flex md6>
                  <v-card style="background-color:#bcbec0;color:#B11117">
                          Total Fertilizer requirement for crop/irrigation type selected for <span class="highlight-input"> {{area_hectare}} hectare(s) </span> <br>
                          N: <span  class="highlight-input"> {{ NPK_total.N_total  }} </span> &nbsp kg/ha &nbsp &nbsp
                          P: <span  class="highlight-input"> {{ NPK_total.P_total }} </span>  &nbsp kg/ha &nbsp &nbsp
                          K: <span  class="highlight-input"> {{ NPK_total.K_total }} </span>  &nbsp kg/ha <br>

                    <!-- <div id="pie-chart-1"> </div> -->
                  </v-card>
                </v-flex>

                <v-flex md6>
                  <v-card style="background-color:#bcbec0;color:#B11117">
                    N,P,K fertilization further required for your soil based on your soil test result: <br>
                    N: <span  class="highlight-input"> {{ NPK_deficit.N_deficit  }} </span> &nbsp kg  &nbsp
                    P: <span  class="highlight-input"> {{ NPK_deficit.P_deficit }} </span> &nbsp kg  &nbsp
                    K: <span  class="highlight-input"> {{ NPK_deficit.K_deficit }} </span> &nbsp kg  &nbsp
                <br>

                <!-- <div id="pie-chart-2"></div> -->
                  </v-card>
                </v-flex>
              </v-layout>
            </div>

            <div class="text-md-center">
              <v-btn round justify-center :to="{name: 'FertilizerOptimizer'}" :disabled="disable_button"> NEXT </v-btn>
            </div>
            <br>
      <div class="page-footer">
        This app has been developed as a part of "A Model of Comprehensive Agribusiness Extension Service in Karnataka (CABES)", Department of Agriculture, Government of Karnataka
    </div>
    </div>

</template>

<script>
// import { generate_pie_chart } from '../charts/Piechart';
import { fetchMicronutrientData} from '../reducers/FetchServerData';
import _ from 'lodash';
import * as d3plus from "d3plus";
import API from '../reducers/API'

  export default {
    name: 'Home',
    data () {
      return {
        selected_crop:'',
        selected_irrigation_type:'',
        irrigation_type_list:[],
        area_hectare:0,
        disable_button:true,
        NPK_soil_test_result:{
          N_soil_test_result:0,
          P_soil_test_result:0,
          K_soil_test_result:0
        },
        // piechart_view:0,
        // deficit_chart_view:0,
        NPK_per_hectare:{
          N_per_hectare:0,
          P_per_hectare:0,
          K_per_hectare:0
        },
        NPK_total:{
          N_total:0,
          P_total:0,
          K_total:0
        },
        NPK_deficit:{
          N_deficit:0,
          P_deficit:0,
          K_deficit:0
        }
        // },
        // Chartdata:[
        //   {"value": 0, "name": "Nitrogen", "hex": "#1f6359"},
        //   {"value": 0, "name": "Phosphorus", "hex": "#B11117"},
        //   {"value": 0, "name": "Potassium", "hex": "#4bc1a4"}
        // ],
      }
    },
    created : function () {
      fetchMicronutrientData(this.$store);
      },
      mounted : function(){
        this.$store.selects.NPK_total = {}
        this.$store.selects.NPK_deficit = {}
        this.$store.selects.NPK_per_hectare = {}
        this.$store.selects.NPK_soil_test_result = {}
      },
    methods:{
      fertilizer_calc(){

        if (!isNaN(this.area_hectare) && this.area_hectare > 0){
          var g = this.$store.api.micronutrient_dtl_json;
          var o = _.filter(g,{"crop_name": this.$store.selects.crop_name, "irrigation_type_code": this.$store.selects.irrigation_type_code});
          console.log(o)

          this.NPK_per_hectare.N_per_hectare = o[0].N_per_hectare;
          this.NPK_per_hectare.P_per_hectare = o[0].P_per_hectare;
          this.NPK_per_hectare.K_per_hectare = o[0].K_per_hectare;

          this.$store.selects.NPK_total.N_total = this.area_hectare * o[0].N_per_hectare;
          this.$store.selects.NPK_total.P_total = this.area_hectare * o[0].P_per_hectare;
          this.$store.selects.NPK_total.K_total = this.area_hectare * o[0].K_per_hectare;
          this.NPK_total = this.$store.selects.NPK_total

        //generate chart
          // this.piechart_view = generate_pie_chart(this.piechart_view,'#pie-chart-1',this.Chartdata);
          // this.piechart_view.draw();
          }
        else{
          alert("INVALID INPUT: Enter a numeric input greater than 0 for area in hectares");
          this.area_hectare = 0;
        }
      },
      update_N_deficit(){
        this.$store.selects.NPK_soil_test_result.N_soil_test_result = this.N_soil_test_result;
        console.log(this.$store.selects.NPK_soil_test_result.N_soil_test_result)
      },
      update_P_deficit(){
        this.$store.selects.NPK_soil_test_result.P_soil_test_result = this.P_soil_test_result;
        console.log(this.$store.selects.NPK_soil_test_result.P_soil_test_result)
      },
      update_K_deficit(){
        this.$store.selects.NPK_soil_test_result.K_soil_test_result = this.K_soil_test_result;
        console.log(this.$store.selects.NPK_soil_test_result.K_soil_test_result)
      },
      generate_deficit_chart(){
        if (this.NPK_soil_test_result.N_soil_test_result == 0 || this.NPK_soil_test_result.N_soil_test_result == null) {
          console.log("into zero N")
          this.$store.selects.NPK_soil_test_result.N_soil_test_result = 0
        }
        if (this.NPK_soil_test_result.P_soil_test_result == 0  || this.NPK_soil_test_result.P_soil_test_result == null) {
          console.log("into zero P")
          this.$store.selects.NPK_soil_test_result.P_soil_test_result = 0
        }
        if (this.NPK_soil_test_result.K_soil_test_result == 0  || this.NPK_soil_test_result.K_soil_test_result == null) {
          console.log("into zero K")
          this.$store.selects.NPK_soil_test_result.K_soil_test_result = 0
        }

        this.$store.selects.NPK_deficit.N_deficit = this.$store.selects.NPK_total.N_total - this.NPK_soil_test_result.N_soil_test_result;
        this.$store.selects.NPK_deficit.P_deficit = this.$store.selects.NPK_total.P_total - this.NPK_soil_test_result.P_soil_test_result;
        this.$store.selects.NPK_deficit.K_deficit = this.$store.selects.NPK_total.K_total - this.NPK_soil_test_result.K_soil_test_result;

        if (this.$store.selects.NPK_deficit.N_deficit < 0){
          this.NPK_deficit.N_deficit = this.$store.selects.NPK_deficit.N_deficit = 0
        }
        if (this.$store.selects.NPK_deficit.P_deficit < 0){
          this.NPK_deficit.P_deficit = this.$store.selects.NPK_deficit.P_deficit = 0
        }
        if (this.$store.selects.NPK_deficit.K_deficit < 0){
          this.NPK_deficit.K_deficit = this.$store.selects.NPK_deficit.K_deficit = 0
        }


        // this.Chartdata[0].value = this.$store.selects.NPK_deficit.N_deficit
        // this.Chartdata[1].value = this.$store.selects.NPK_deficit.P_deficit
        // this.Chartdata[2].value = this.$store.selects.NPK_deficit.K_deficit

        this.NPK_deficit = this.$store.selects.NPK_deficit

        console.log(this.NPK_deficit)

        //generate chart
        // this.deficit_chart_view = generate_pie_chart(this.deficit_chart_view,'#pie-chart-2',this.Chartdata)
        // this.deficit_chart_view.draw()
        this.validate_inputs()
      },
      validate_inputs(){
        if (!(this.selected_crop) || !(this.selected_irrigation_type) || (this.area_hectare <= 0)){
          this.disable_button = true;
        } else{
          this.disable_button = false;
        }
      }
    },
    computed: {
      crop_select: function(){
        var g = this.$store.api.micronutrient_dtl_json
        var crop_name_list = []
        for (var i=0;i<g.length;i++){
          crop_name_list.push(g[i].crop_name)
          }
        this.fertilizer_list = this.$store.api.fertilizer_dtl_json
        return Array.from(new Set(crop_name_list))
      },
      irrigation_type_select: function(){
        //get the irrigation type for the given crop name
        var g = this.$store.api.micronutrient_dtl_json
        var o = _.filter(g,{'crop_name': this.$store.selects.crop_name});
        this.irrigation_type_list = _.map(o,'irrigation_type_code')
        return this.irrigation_type_list
      }
    },
    watch:{
      selected_crop: function(val){
        this.$store.selects.crop_name = val
        },
      selected_irrigation_type: function(val){
        this.$store.selects.irrigation_type_code = val
        }
      }
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

@import '../stylesheet/stylesheet.css'

</style>
