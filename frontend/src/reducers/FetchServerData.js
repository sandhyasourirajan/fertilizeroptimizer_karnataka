import axios from 'axios'

export function fetchMicronutrientData (store) {

    const path = `http://localhost:8000/micronutrient`

    axios.get(path)
        .then(response => {
            store.api.micronutrient_dtl_json = response.data.micronutrient
            // console.log(response.data.micronutrient)
        })
        .catch(error => {
            console.log(error)
        })
}

export function fetchFertilizerData (store) {

    const path = `http://localhost:8000/fertilizer`

    axios.get(path)
        .then(response => {
            store.api.fertilizer_dtl_json = response.data.fertilizer
            // console.log(store.api.fertilizer_dtl_json)
        })
        .catch(error => {
            console.log(error)
        })
}

export function fetchOptimizedData (store,args) {

    const path = `http://localhost:8000/optimize`
    // console.log(args)
    axios.post(path,args)
        .then(response => {
            store.api.optimized_output = response.data.optimized_output
        })
        .catch(error => {
            console.log(error)
        })

        return
}
