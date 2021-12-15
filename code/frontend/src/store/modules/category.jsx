import { createSlice } from '@reduxjs/toolkit';


const initialState = {
  category: '영상별 분석',
};

// Define Actions & Reducer
const categorySlice = createSlice({
  name: 'category',
  initialState,
  reducers: {
    selectCategory(state, action) {
      state.category = action.payload;
  },
}}
);

export const categoryActions = categorySlice.actions;
export const nowCategory = state => state.category;
export default categorySlice.reducer;
