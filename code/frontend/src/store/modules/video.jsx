import { createSlice } from "@reduxjs/toolkit";
import axios from "axios";

// Define Actions & Reducer
const videoSlice = createSlice({
  name: "videos",
  initialState: {
    videoList: [],
    videoListLength: 0,
    nextVideoPage: "",
    prevVideoPage: "",
  },
  reducers: {
    setPrevVideoPage: (state, action) => {
      state.prevVideoPage = action.payload;
    },
    setNextVideoPage: (state, action) => {
      state.nextVideoPage = action.payload;
    },
    updateVideoList: (state, action) => {
      state.videoList = action.payload;
    },
    updateVideoListLength: (state, action) => {
      state.videoListLength = action.payload;
    },
    selectVideo: (state, action) => {
      state.videoList.videoList[action.payload] = !state.videoList.videoList[action.payload];
    },
    closeVideo: (state, action) => {
      state.videoList.videoList[action.payload] = false;
    },
    selectAllVideo: (state, action) => {
      state.videoList.videoList[action.payload] = true;
    },
    resetVideo: (state) => {
      state.videoList = [];
      state.videoListLength = 0;
      state.nextVideoPage = "";
      state.prevVideoPage = "";
    },
  },
});

export const videoSliceActions = videoSlice.actions;
export const nowVideoList = (state) => state.videoSlice.videoList;
export const nowVideoListLength = (state) => state.videoSlice.videoListLength;
export const nowNextVideoPage = (state) => state.videoSlice.nextVideoPage;
export const nowPrevVideoPage = (state) => state.videoSlice.prevVideoPage;
export default videoSlice.reducer;
