import { call, put, select, takeLatest } from "redux-saga/effects";
import { ReducerType } from ".";
import { contentsFeedBackActions } from "./contentsFeedBack";
import axios from "axios";
import { create } from "domain";

const delay = (time: number) =>
  new Promise((resolve) => {
    setTimeout(resolve, time);
  });

const createFormData = (state: any) => {
  const data = new FormData();
  data.append("channel_id", state.user.channelId);
  data.append("video_list", state.contentsFeedBack.selectedVideosId);

  return data;
};

function predictAPI(data: FormData) {
  axios
    .post(process.env.REACT_APP_BACKEND_URL + "/api/analysis/predict", data, {
      headers: {
        Authorization: `Bearer ${window.localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      console.log(response.data.analysis_id);
      const analysis_id = response.data.analysis_id;
      contentsFeedBackActions.saveAnalysisId(analysis_id);
      const request = setInterval(function () {
        axios
          .get(process.env.REACT_APP_BACKEND_URL + "/api/analysis/result/" + analysis_id, {
            headers: {
              Authorization: `Bearer ${window.localStorage.getItem("token")}`,
            },
          })
          .then((response) => {
            console.log(response.data);
            if (response.data.state === "SUCCESS") {
              clearInterval(request);
              console.log("finish");
            }
          })
          .catch((error) => {
            console.log(error.data);
          });
      }, 10000);
    });
}

function* getAnalysisResult() {
  const data: FormData = yield select<any>(createFormData);
  yield call<any>(predictAPI(data));
}

function* getTest() {
  try {
    yield call(getAnalysisResult);
    yield put(contentsFeedBackActions.outContentsFeedBack(Boolean(false)));
  } catch (error) {
    yield put(contentsFeedBackActions.outContentsFeedBack(Boolean(false)));
  }

  // yield call(delay, 10000);
  // yield put(contentsFeedBackActions.outContentsFeedBack(Boolean(false)));
}

function* testSaga() {
  yield takeLatest(contentsFeedBackActions.enterContentsFeedBack, getTest);
}

export default testSaga;
