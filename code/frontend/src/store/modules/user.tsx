import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface User {
  email: string;
  name: string;
  img_url: string;
}

interface InputUserInfo {
  inputName: string;
  nickName: string;
}

interface InputChannelInfo {
  category: string[];
  categoryNumList: number[];
  upload_term: number;
}

interface LoginSuccess {
  success: boolean;
}

interface AllUserInfo {
  email: string;
  name: string;
  img_url: string;
  nickName: string;
  category: string[];
  categoryNumList?: number[];
  upload_term: number;
  inputName: string;
}

interface ChannelInfo {
  channelId: string;
  channelTitle: string;
  channelUrl: string;
  channelImgUrl: string;
}

const initialState = {
  email: "",
  name: "",
  img_url: "",
  nickName: "",
  inputName: "",
  category: [] as string[],
  categoryNumList: [] as number[],
  upload_term: 0,
  channelId: "",
  channelTitle: "",
  channelUrl: "",
  channelImgUrl: "",
  success: Boolean(false),
};

// Define Actions & Reducer
const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    saveUser(state, action: PayloadAction<User>) {
      const { email, name, img_url } = action.payload;
      state.email = email;
      state.name = name;
      state.img_url = img_url;
    },
    saveName(state, action: PayloadAction<InputUserInfo>) {
      const { inputName, nickName } = action.payload;
      state.inputName = inputName;
      state.nickName = nickName;
    },
    saveChannelInfo(state, action: PayloadAction<InputChannelInfo>) {
      const { category, categoryNumList, upload_term } = action.payload;
      state.upload_term = upload_term;
      state.categoryNumList = [...categoryNumList];
      state.category = [...category];
    },
    loginSuccess(state, action: PayloadAction<LoginSuccess>) {
      const { success } = action.payload;
      state.success = success;
    },
    saveAllUserInfo(state, action: PayloadAction<AllUserInfo>) {
      const { email, name, img_url, nickName, category, upload_term, inputName } = action.payload;
      if (action.payload.categoryNumList) {
        const categoryNumList = action.payload.categoryNumList;
        state.categoryNumList = [...categoryNumList];
      }
      state.email = email;
      state.name = name;
      state.img_url = img_url;
      state.nickName = nickName;
      state.upload_term = upload_term;
      state.category = [...category];

      state.inputName = inputName;
    },
    saveYoutubeInfo(state, action: PayloadAction<ChannelInfo>) {
      const { channelId, channelTitle, channelUrl, channelImgUrl } = action.payload;
      state.channelId = channelId;
      state.channelTitle = channelTitle;
      state.channelUrl = channelUrl;
      state.channelImgUrl = channelImgUrl;
    },
    resetUserInfo(state) {
      state.email = "";
      state.name = "";
      state.img_url = "";
      state.nickName = "";
      state.inputName = "";
      state.category = [] as string[];
      state.categoryNumList = [] as number[];
      state.upload_term = 0;
      state.channelId = "";
      state.channelTitle = "";
      state.channelUrl = "";
      state.channelImgUrl = "";
      state.success = Boolean(false);
    },
  },
});

export const userActions = userSlice.actions;
export default userSlice.reducer;
