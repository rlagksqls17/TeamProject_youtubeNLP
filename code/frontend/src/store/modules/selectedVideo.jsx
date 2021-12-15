import { createSlice } from "@reduxjs/toolkit";

// Define Actions & Reducer
const selectedVideoSlice = createSlice({
  name: "selectedVideos",
  initialState: {
    selectedVideoList: [],
    selectedVideoListLength: 0,
  },
  reducers: {
    updateSelectedVideoListLength: (state, action) => {
      state.selectedVideoListLength = action.payload;
    },
    updateSelectedVideoList: (state, action) => {
      state.selectedVideoList = action.payload;
    },
    selectSelectedVideo: (state, action) => {
      state.selectedVideoList.selectedVideoList[action.payload] = !state.selectedVideoList.selectedVideoList[action.payload];
    },
    closeSelectedVideo: (state, action) => {
      state.selectedVideoList.selectedVideoList[action.payload] = false;
    },
    selectAllSelectedVideo: (state, action) => {
      state.selectedVideoList.selectedVideoList[action.payload] = true;
    },
    resetSelectedVideo: (state) => {
      state.selectedVideoList = [];
      state.selectedVideoListLength = 0;
    },
  },
});

export const selectedVideoSliceActions = selectedVideoSlice.actions;
export const nowSelectedVideoList = (state) => state.selectedVideoSlice.selectedVideoList;
export const nowSelectedVideoListLength = (state) => state.selectedVideoSlice.selectedVideoListLength;
export default selectedVideoSlice.reducer;
