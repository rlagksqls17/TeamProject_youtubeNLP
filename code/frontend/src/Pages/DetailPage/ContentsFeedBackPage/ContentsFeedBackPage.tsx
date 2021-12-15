import React, { useEffect, useState } from "react";
import styles from "./ContentsFeedBackPage.module.scss";
import classNames from "classnames/bind";
import { Sidebar } from "Components/common";
import SearchBar from "Components/SearchBar/SearchBar/SearchBar";
import { useDispatch, useSelector } from "react-redux";
import { actions, ReducerType } from "store/modules";
import { nowCategory } from "store/modules/category";
import PieChartC from "Components/PieChart/PieChart";

const cx = classNames.bind(styles);

const gameData = [
  { name: "배틀그라운드", value: 600 },
  { name: "리그오브레전드", value: 500 },
  { name: "카트라이더", value: 40 },
  { name: "오버워치", value: 40 },
  { name: "리니지", value: 200 },
  { name: "서든어택", value: 120 },
  { name: "로스트아크", value: 120 },
  { name: "피파 온라인", value: 80 },
  { name: "메이플스토리", value: 150 },
  { name: "스타크래프트", value: 100 },
];

function ContentsFeedBackPage() {
  const dispatch = useDispatch();
  const isCategorySelect = useSelector(nowCategory);
  const finishAnalysis = useSelector((state: ReducerType) => state.contentsFeedBack.IsEnter);
  const [isSelectedCommentArray, setIsSelectedCommentArray] = useState([]);

  const requestAnalysis = () => {
    alert("분석결과요청");
    dispatch(actions.enterContentsFeedBack(Boolean(true)));
  };

  const outRequest = () => {
    dispatch(actions.outContentsFeedBack(Boolean(false)));
  };

  useEffect(() => {
    if (finishAnalysis === false) alert("Finish Analysis!");
  }, [finishAnalysis]);

  useEffect(() => {
    console.log(isCategorySelect);
  }, [isCategorySelect]);

  return (
    <div className={cx("contentsFeedbackContainer")}>
      <div className={cx("sideBarContainer")}>
        <Sidebar id={8} />
        <div className={cx("sideLine")}></div>
      </div>
      <div className={cx("contentsContainer")}>
        <div className={cx("contentsFeedbackTitle")}>컨텐츠 요구 분석 페이지</div>
        <button onClick={requestAnalysis}>분석결과 요청</button>
        <button onClick={outRequest}>나가기</button>
        <div className={cx("contentsFeedbackDesc")}>시청자들의 요구 피드백이 담긴 댓글 분석 결과</div>
        <div className={cx("contentsFBBox")}>
          <div className={cx("contentsFBSearch")}>
            <SearchBar />
          </div>
          <div className={cx("pieChartFBBox")}>
            <div className={cx("pieChartFB")}>
              <PieChartC data={gameData} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ContentsFeedBackPage;
