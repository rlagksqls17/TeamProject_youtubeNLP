import React, { Fragment, useEffect, useState } from "react";
import { RootStateOrAny, useDispatch, useSelector } from "react-redux";
import { Navbar, Sidebar } from "../../../Components/common";
import SearchBar from "../../../Components/SearchBar/SearchBar/SearchBar";
import classNames from "classnames/bind";
import styles from "./AllFeedBackPage.module.scss";
import { nowCategory } from "../../../store/modules/category";
import { Link } from "react-router-dom";
import ROUTES from "../../../constants/routes";
import { actions } from "../../../store/modules";
import AllBarChart from "../../../Components/barChart/AllBarChart";
import AllLineChart from "../../../Components/LineChart/AllLineChart";
import axios from "axios";
import { nowAllTenArray, nowAnalysis } from "store/modules/analysis";

const cx = classNames.bind(styles);

function AllFeedBackPage() {
  const [thisData, setThisData] = useState([]);
  const [thissData, setThissData] = useState([]);
  const [sortByViewCount, setSortByViewCount] = useState([]);
  const [isSelectedCommentArray, setIsSelectedCommentArray] = useState([]);
  const nowAllTen = useSelector(nowAllTenArray);
  const isAnalysis = useSelector(nowAnalysis);
  const clusterId = isAnalysis.analysisArray.clusters[0].id;

  const getUserInfo = () => {
    axios
      .get(process.env.REACT_APP_BACKEND_URL + `/api/comments/${clusterId}`, {
        headers: {
          Authorization: `Bearer ${window.localStorage.getItem("token")}`,
        },
      })
      .then((response) => {
        const result = response.data.sort(function (a, b) {
          return a.video.view_count - b.video.view_count;
        });
        let obj = result.reduce((res, curr) => {
          if (res[curr.video.view_count]) res[curr.video.view_count].push(curr);
          else Object.assign(res, { [curr.video.view_count]: [curr] });
          return res;
        }, {});
        console.log(result);
        setSortByViewCount(obj);
        console.log(obj);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  async function getFeedBackList() {
    setThisData(nowAllTen);
    setIsSelectedCommentArray(Array.from({ length: nowAllTen.length }, (v, i) => false));
    console.log(nowAllTen.length);
  }

  useEffect(() => {
    getUserInfo();
    getFeedBackList();
  }, []);

  const dispatch = useDispatch();
  const isCategorySelect = useSelector(nowCategory);

  const name = useSelector((state) => state.user.nickName);

  const setVideo = () => {
    dispatch(actions.selectCategory("영상별 분석"));
  };

  const setSelect = (number) => {
    let newArr = [...isSelectedCommentArray];
    newArr[number] = !isSelectedCommentArray[number];
    setIsSelectedCommentArray(newArr);
    console.log(newArr);
    let testArr = [...isSelectedCommentArray];
    setThissData(thissData.concat(testArr));
    console.log(thissData);
  };

  return (
    <Fragment>
      <div className={cx("feedBackContainer")}>
        <Sidebar id={3} />
        <div className={cx("sideLine")}></div>
        <div className={cx("feedBackWrap")}>
          <div className={cx("feedBackWrapHeader")}>
            <div className={cx("feedBackText")}>
              <div className={cx("feedBackTitle")}>반갑습니다 {name}님!</div>
              <div className={cx("feedBackDescription")}>댓글들을 분석하고 사용자들의 피드백을 확인해보세요!</div>
            </div>
          </div>
          <div></div>
          <div className={cx("feedBackContentWrap")}>
            <Link className={cx("allFeedbackSelected")} to={ROUTES.ALLFEEDBACK} onClick={setVideo}>
              모든 피드백
            </Link>
            <Link className={cx("posFeedbackSelect")} to={ROUTES.POSFEEDBACK} onClick={setVideo}>
              긍정 피드백
            </Link>
            <Link className={cx("negFeedbackSelect")} to={ROUTES.NEGFEEDBACK} onClick={setVideo}>
              부정 피드백
            </Link>
            <div className={cx("feedBackContent")}>
              <div className={cx("feedBackPageSearch")}>
                <SearchBar />
              </div>
              <div className={cx("feedBackPageContainer")}>
                <div className={cx("feedBackPageLeft")}>
                  <div></div>
                  <div></div>
                  <div className={cx("feedBackBarGrpah")}>
                    {isCategorySelect.category === "영상별 분석" ? <AllBarChart /> : <AllLineChart />}
                  </div>
                  <div>
                    <div className={cx("allBarChart")}>
                      {thisData.map((data, i) => {
                        return (
                          <div className={cx("chartWrap")}>
                            <div className={cx("chartLeft")}>{i + 1}.</div>
                            <div className={cx("chartRight")}>{data.name}</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
                <div className={cx("feedBackPageRight")}>
                  <div></div>
                  <div className={cx("feedBackCommentsContatiner")}>
                    <div className={cx("feedBackCommentsHeader")}>
                      <div>순위</div>
                      <div>피드백</div>
                      <div>총 댓글 수</div>
                      <div>좋아요</div>
                    </div>
                    <div className={cx("feedBackComments")}>
                      {thisData.map((data, i) => {
                        return (
                          <>
                            <div className={cx("feedBackComment")} id={i} onClick={() => setSelect(i)}>
                              <div style={{ overflow: "hidden", height: "50px" }}>{data.id}위</div>
                              <div style={{ overflow: "hidden", height: "50px" }}>{data.name}</div>
                              <div style={{ overflow: "hidden", height: "50px" }}>{data.댓글수} 개</div>
                              <div style={{ overflow: "hidden", height: "50px" }}>{data.좋아요수} 개</div>
                            </div>
                            {isSelectedCommentArray[i] ? (
                              <div>
                                <div className={cx("feedBackDetailHeader")}>
                                  <div>댓글이 달린 영상</div>
                                  <div>원래 댓글</div>
                                  <div>댓글 작성 일자</div>
                                  <div>좋아요</div>
                                  <div>조회수</div>
                                </div>
                                {sortByViewCount[thisData[i].top_comment.video.view_count].map((sortData, j) => {
                                  return (
                                    <div className={cx("feedBackDetail")}>
                                      <div style={{ overflow: "hidden", height: "20px" }}>
                                        {sortByViewCount[thisData[i].top_comment.video.view_count][j].video.title}
                                      </div>
                                      <div style={{ overflow: "hidden", height: "20px" }}>
                                        {sortByViewCount[thisData[i].top_comment.video.view_count][j].text_original}
                                      </div>
                                      <div style={{ overflow: "hidden", height: "20px" }}>
                                        {sortByViewCount[thisData[i].top_comment.video.view_count][j].published_at}
                                      </div>
                                      <div style={{ overflow: "hidden", height: "20px" }}>
                                        {sortByViewCount[thisData[i].top_comment.video.view_count][j].like_count}
                                      </div>
                                      <div style={{ overflow: "hidden", height: "20px" }}>
                                        {sortByViewCount[thisData[i].top_comment.video.view_count][j].video.view_count}
                                      </div>
                                    </div>
                                  );
                                })}
                                )
                              </div>
                            ) : null}
                          </>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Fragment>
  );
}

export default AllFeedBackPage;
