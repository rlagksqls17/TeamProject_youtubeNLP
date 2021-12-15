import React from "react";
import styles from "./DashBoard.module.scss";
import classNames from "classnames/bind";
import PieChartC from "../../../Components/PieChart/PieChart";
import { nowCategory } from "../../../store/modules/category";
import PosLineChart from "../../../Components/LineChart/PosLineChart";
import NegLineChart from "../../../Components/LineChart/NegLineChart";
import AllLineChart from "../../../Components/LineChart/AllLineChart";

const cx = classNames.bind(styles);

function DashBoardComment() {
  const thisData = [
    {
      id: 1,
      name: "소리가 너무 커요",
      댓글수: 300,
      좋아요수: 240,
      box: 10,
    },
    {
      id: 2,
      name: "자막 틀렸어요",
      댓글수: 400,
      좋아요수: 138,
      box: 10,
    },
    {
      id: 3,
      name: "진짜 맛있어 보이네요",
      댓글수: 200,
      좋아요수: 98,
      box: 10,
    },
    {
      id: 4,
      name: "먹방 잘 찍으시네요",
      댓글수: 278,
      좋아요수: 98,
      box: 10,
    },
    {
      id: 5,
      name: "치킨먹어주세요",
      댓글수: 189,
      좋아요수: 80,
      box: 10,
    },
    {
      id: 6,
      name: "자세한 설명 굿",
      댓글수: 239,
      좋아요수: 180,
      box: 10,
    },
    {
      id: 7,
      name: "구독 누르고 갑니다",
      댓글수: 349,
      좋아요수: 230,
      box: 10,
    },
    {
      id: 8,
      name: "진짜 웃기다",
      댓글수: 189,
      좋아요수: 80,
      box: 10,
    },
    {
      id: 9,
      name: "화질 너무 구려요",
      댓글수: 239,
      좋아요수: 138,
      box: 10,
    },
    {
      id: 10,
      name: "음질이 너무 안좋아요",
      댓글수: 349,
      좋아요수: 243,
      box: 10,
    },
  ];

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

  return (
    <>
      <div className={cx("dashBoardWrapMiddle")}>
        <div className={cx("dashBoardAllFeedback")}>
          <p className={cx("dashP")}>모든 피드백</p>
          <div className={cx("squareWrap")}>
            <div className={cx("allSquareLike")}></div>
            <p className={cx("allSquareP")}>좋아요 수</p>
            <div className={cx("allSquareComment")}></div>
            <p className={cx("allSquareP")}>댓글 수</p>
          </div>
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
          <div className={cx("allBarGraph")}>
            <AllLineChart />
          </div>
        </div>
        <div className={cx("dashBoardWrapMiddleBlank")}></div>
        <div className={cx("dashBoardAllFeedback")}>
          <p className={cx("dashP")}>사용자 요구 분석</p>

          <div className={cx("allBarChart")}>
            {gameData.map((data, i) => {
              return (
                <div className={cx("chartWrap")}>
                  <div className={cx("chartLeft")}>{i + 1}.</div>
                  <div className={cx("chartRight")}>{data.name}</div>
                </div>
              );
            })}
          </div>
          <div className={cx("pieGraph")}>
            <PieChartC data={gameData} />
          </div>
        </div>
      </div>
      <div className={cx("dashBoardWrapDown")}>
        <div className={cx("dashBoardWrapDownGrid")}>
          <div className={cx("dashBoardPosFeedback")}>
            <p className={cx("dashP")}>긍정 피드백</p>
            <div className={cx("squareWrap")}>
              <div className={cx("posSquareLike")}></div>
              <p className={cx("posSquareP")}>좋아요 수</p>
              <div className={cx("posSquareComment")}></div>
              <p className={cx("posSquareP")}>댓글 수</p>
            </div>
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
            <div className={cx("allBarGraph")}>
              <PosLineChart />
            </div>
          </div>
          <div className={cx("dashBoardWrapDownBlank")}>
            <div className={cx("BlankLine")}></div>
          </div>
          <div className={cx("dashBoardPosFeedback")}>
            <p className={cx("dashP")}>부정 피드백</p>
            <div className={cx("squareWrap")}>
              <div className={cx("negSquareLike")}></div>
              <p className={cx("negSquareP")}>좋아요 수</p>
              <div className={cx("negSquareComment")}></div>
              <p className={cx("negSquareP")}>댓글 수</p>
            </div>
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
            <div className={cx("allBarGraph")}>
              <NegLineChart />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default DashBoardComment;
