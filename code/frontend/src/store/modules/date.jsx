import { createSlice } from '@reduxjs/toolkit';


const initialState = {
  startDate: new Date(),
  endDate: new Date(),
};

// Define Actions & Reducer
const dateSlice = createSlice({
  name: 'date',
  initialState,
  reducers: {
    saveDate(state, action) {
      const { startDate, endDate } = action.payload;
      state.startDate = startDate;
      state.endDate = endDate;
    },
  },
});

export const dateActions = dateSlice.actions;
export const nowDate = state => [state.date.startDate,state.date.endDate];
export const nowStartDate = state => state.date.startDate;
export const nowEndDate = state => state.date.endDate;
export default dateSlice.reducer;
