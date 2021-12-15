import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  analysisArray: [],
  allTenArray: [],
  posFiveArray: [],
  negFiveArray: [],
  loading: false,
};

// Define Actions & Reducer
const analysisSlice = createSlice({
  name: "analysis",
  initialState,
  reducers: {
    setAnalysis(state, action) {
      state.analysisArray = action.payload;
    },
    setAllTen(state, action) {
      state.allTenArray = action.payload;
    },
    setNegFive(state, action) {
      state.negFiveArray = action.payload;
    },
    setPosFive(state, action) {
      state.posFiveArray = action.payload;
    },
    setLoading(state, action) {
      state.loading = action.payload;
    },
    resetAnalysisData(state) {
      state.analysisArray = [];
      state.allTenArray = [];
      state.negFiveArray = [];
      state.posFiveArray = [];
      state.loading = false;
    },
  },
});

export const analysisActions = analysisSlice.actions;
export const nowAnalysis = (state) => state.analysis;
export const nowAllTenArray = (state) => state.analysis.allTenArray;
export const nowNegFiveArray = (state) => state.analysis.negFiveArray;
export const nowPogFiveArray = (state) => state.analysis.posFiveArray;
export const nowLoading = (state) => state.loading;
export default analysisSlice.reducer;
