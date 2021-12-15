import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface selectedVideosId {
  selectedVideosId: string[];
}

const initialState = {
  selectedVideosId: [] as string[],
  analysisData: {},
  analysis_id: "",
  IsEnter: Boolean(false),
};

// Define Actions & Reducer
const contentsFeedBackSlice = createSlice({
  name: "contentsFeedBack",
  initialState,
  reducers: {
    enterContentsFeedBack(state, action: PayloadAction<boolean>) {
      state.IsEnter = action.payload;
    },
    outContentsFeedBack(state, action: PayloadAction<boolean>) {
      state.IsEnter = action.payload;
    },
    saveSelectedVideosId(state, action: PayloadAction<selectedVideosId>) {
      const { selectedVideosId } = action.payload;
      state.selectedVideosId = [...selectedVideosId];
    },
    saveAnalysisId(state, action: PayloadAction<string>) {
      state.analysis_id = action.payload;
    },
  },
});

export const contentsFeedBackActions = contentsFeedBackSlice.actions;
export default contentsFeedBackSlice.reducer;
