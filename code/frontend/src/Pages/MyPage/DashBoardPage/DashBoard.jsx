import { useEffect, useState } from "react";
import React from "react";
import styles from "./DashBoard.module.scss";
import classNames from "classnames/bind";
import { Sidebar } from "../../../Components/common";
import SearchBar from "../../../Components/SearchBar/SearchBar/SearchBar.jsx";
import { actions } from "../../../store/modules";
import { useSelector, useDispatch } from "react-redux";
import { nowCategory } from "../../../store/modules/category";
import { nowVideoList, nowNextVideoPage, nowPrevVideoPage } from "../../../store/modules/video";
import DashBoardVideo from "./DashBoardVideo";
import DashBoardComment from "./DashBoardComment";
import axios from "axios";
import { nowAllTenArray, nowAnalysis, nowNegFiveArray, nowPogFiveArray } from "store/modules/analysis";
import { Hypnosis } from "react-cssfx-loading";

const cx = classNames.bind(styles);

function DashBoard() {
  const [isloading, setIsLoading] = useState(true);

  const [videoString, setVideoString] = useState("");
  const dispatch = useDispatch();
  const isCategorySelect = useSelector(nowCategory);
  const isAnalysis = useSelector(nowAnalysis);
  const nowLoading = useSelector(nowAnalysis).loading;
  const name = useSelector((state) => state.user.nickName);
  console.log(nowLoading);
  const isNextVideoPage = useSelector(nowNextVideoPage);
  const isPrevVideoPage = useSelector(nowPrevVideoPage);
  const isVideoList = useSelector(nowVideoList);

  const user = useSelector((state) => state.user);
  const channel_id = user.channelUrl.substring(32);
  const uploadTerm = user.upload_term;
  const config = {
    headers: {
      Authorization: `Bearer ${window.localStorage.getItem("token")}`,
    },
  };

  async function getVideos() {
    const response = await axios
      .get(process.env.REACT_APP_BACKEND_URL + `/api/videos?channel_id=${channel_id}&page_token=${isNextVideoPage}`, config)
      .then((response) => {
        if (response.data.prev_page_token == null) {
          console.log(response.data);
          dispatch(actions.updateSelectedVideoList({ selectedVideoList: Array(response.data.page_info.totalResults).fill(false) }));
          dispatch(actions.updateVideoList(response.data.video_items));
          dispatch(actions.setNextVideoPage(response.data.next_page_token));
          console.log(response.data.video_items);
          const analyticData = new FormData();
          const newArray = [];
          if (uploadTerm === 1) {
            setVideoString(response.data.video_items.slice(0, 10));
            const upLoadTermDay = response.data.video_items.slice(0, 10);
            for (let i = 0; i < upLoadTermDay.length; i++) {
              newArray.push(response.data.video_items[i]["id"]);
            }
            analyticData.append("channel_id", channel_id);
            analyticData.append("video_list", newArray.join());
          } else if (uploadTerm === 2) {
            setVideoString(response.data.video_items.slice(0, 4));
            const upLoadTermWeek = response.data.video_items.slice(0, 4);
            for (let i = 0; i < upLoadTermWeek.length; i++) {
              newArray.push(response.data.video_items[i]["id"]);
              console.log(response.data.video_items[i]["id"]);
            }
            analyticData.append("channel_id", channel_id.toString());
            analyticData.append("video_list", newArray.toString());
          } else if (uploadTerm === 3) {
            setVideoString(response.data.video_items[0]["id"]);
            const upLoadTermMonth = response.data.video_items[0]["id"];
            analyticData.append("channel_id", channel_id);
            analyticData.append("video_list", response.data.video_items[0]["id"]);
          }
          axios
            .post(process.env.REACT_APP_BACKEND_URL + "/api/analysis/predict", analyticData, config)
            .then((response) => {
              const analyticDatas = response.data["analysis_id"];
              axios
                .get(process.env.REACT_APP_BACKEND_URL + `/api/analysis/result/${response.data["analysis_id"]}`, config)
                .then((response) => {
                  console.log(response.data.analysis);
                  console.log(response.data.clusters);
                  if (response.data.clusters === null && response.data.analysis === null) {
                    const thisis = setInterval(() => {
                      axios
                        .get(process.env.REACT_APP_BACKEND_URL + `/api/analysis/result/${analyticDatas}`, config)
                        .then((response) => {
                          console.log(response.data.analysis);
                          console.log(response.data.clusters);
                          if (response.data.clusters !== null && response.data.analysis !== null) {
                            dispatch(actions.setAnalysis(response.data));
                            console.log(isAnalysis);
                            clearInterval(thisis);
                            dispatch(actions.setLoading(true));
                          }
                        })
                        .catch((error) => {
                          console.log(error);
                        });
                    }, 1000);
                  }
                })
                .catch((error) => {
                  console.log(error);
                });
            })
            .catch((error) => {
              console.log(error);
            });
        } else if (response.data.prev_page_token != null) {
          let testArr = [...isVideoList];
          dispatch(actions.updateVideoList(testArr.concat(response.data.video_items)));
          dispatch(actions.setNextVideoPage(response.data.next_page_token));
        } else if (isNextVideoPage == null) {
          console.log("Done!");
        }
      })
      .catch((error) => {
        console.log(error);
      });
    console.log(response);
  }

  useEffect(() => {
    getVideos();
  }, [isAnalysis]);

  return (
    <div className={cx("dashBoardContainer")}>
      {nowLoading ? (
        <div className={cx("loadingPage")}>
          <Hypnosis color="#0000008f" width="200px" height="200px" />
        </div>
      ) : null}
      <Sidebar id={1} />
      <div className={cx("sideLine")}></div>
      <div className={cx("dashBoardWrap")}>
        <div className={cx("dashBoardWrapHeader")}>
          <div className={cx("dashBoardText")}>
            <div className={cx("dashBoardTitle")}>반갑습니다 {name}님!</div>
            <div className={cx("dashBoardDescription")}>댓글들을 분석하고 사용자들의 피드백을 확인해보세요!</div>
          </div>
          <div className={cx("dashBoardSearch")}>
            <SearchBar data={1} func={getVideos} />
          </div>
        </div>
        <div></div>
        {isCategorySelect.category === "영상별 분석" ? <DashBoardVideo /> : <DashBoardComment />}
      </div>
    </div>
  );
}

export default DashBoard;
