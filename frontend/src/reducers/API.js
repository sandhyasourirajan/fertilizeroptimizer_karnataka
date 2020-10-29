import ezFetch from 'ez-fetch';

export default {

  // Call the API to fetch the micronutrient details from DB
  fetchMicronutrientData(){
    var fertilizer_list = []
    const API_URL = `http://localhost:8000/micronutrient`
    ezFetch.get(API_URL)
  },


  // Call the API to fetch the fertilizer details from DB
  fetchFertilizerData(){
    const API_URL = `http://localhost:8000/fertilizer`
    return ezFetch.get(API_URL)
  },

  // Call the API to compute the fertilizer combination for an optimal cost
  fetchOptimizedData (args) {
    // console.log("Args:",args)
    const API_URL = `http://localhost:8000/optimize`
    return ezFetch.post(API_URL,args)
  },

  // Add a new fertilizer to DB
  AddFertilizerData (args) {
    // console.log("Args:",args)
    const API_URL = `http://localhost:8000/addfertilizer`
    return ezFetch.post(API_URL,args)
  }

};
