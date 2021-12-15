import React, { Fragment } from "react";
import styles from "./OpenSidebar.module.scss";
import classNames from "classnames/bind";
import { Link } from "react-router-dom";
import ROUTES from "../../../constants/routes";
import { useDispatch, useSelector } from "react-redux";
import { actions } from "../../../store/modules";

const cx = classNames.bind(styles);

function OpenSideBar(props) {
  const dispatch = useDispatch();
  const isActive = props.isActive;
  const colorId = props.id;
  const setVideo = () => {
    dispatch(actions.selectCategory("영상별 분석"));
  };
  const grey = "#2f2f2f50";
  const blue = "#6563FF";

  const propsArray = [2, 3, 4, 5, 8];

  if (isActive === true) {
    return (
      <Fragment>
        <div className={cx("openSideBar")}>
          <div className={cx("openDashboard")}>
            <Link to={ROUTES.DASHBOARD} onClick={setVideo} style={props.id === 1 ? { color: blue } : { color: grey }}>
              대쉬보드
            </Link>
          </div>
          <div className={cx("openContents")}>
            <div className={cx("openContent")}>
              <Link to={ROUTES.ALLFEEDBACK} onClick={setVideo} style={propsArray.includes(props.id) ? { color: blue } : { color: grey }}>
                컨텐츠
              </Link>
            </div>
            <div className={cx("AllFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.ALLFEEDBACK}
                style={[2, 3].includes(props.id) ? { color: blue } : { color: grey }}
              >
                모든 피드백
              </Link>
            </div>
            <div className={cx("PosFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.POSFEEDBACK}
                style={props.id === 4 ? { color: blue } : { color: grey }}
              >
                긍정 피드백
              </Link>
            </div>
            <div className={cx("NegFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.NEGFEEDBACK}
                style={props.id === 5 ? { color: blue } : { color: grey }}
              >
                부정 피드백
              </Link>
            </div>
            <div className={cx("contentsFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.CONTENTSFEEDBACK}
                style={props.id === 8 ? { color: blue } : { color: grey }}
              >
                컨텐츠 요구 분석
              </Link>
            </div>
          </div>
          <div className={cx("openSetting")}>
            <Link to={ROUTES.SETTING} onClick={setVideo} style={props.id === 6 ? { color: blue } : { color: grey }}>
              환경설정
            </Link>
          </div>
          <div className={cx("openNotification")}>
            <Link to={ROUTES.NOTIFICATION} onClick={setVideo} style={props.id === 7 ? { color: blue } : { color: grey }}>
              알림
            </Link>
          </div>
        </div>
      </Fragment>
    );
  } else if (isActive === false) {
    return (
      <Fragment>
        <div className={cx("closeSideBar")}>
          <div className={cx("openDashboard")}>
            <Link to={ROUTES.DASHBOARD} onClick={setVideo} style={props.id === 1 ? { color: blue } : { color: grey }}>
              대쉬보드
            </Link>
          </div>
          <div className={cx("openContents")}>
            <div className={cx("openContent")}>
              <Link to={ROUTES.ALLFEEDBACK} onClick={setVideo} style={propsArray.includes(props.id) ? { color: blue } : { color: grey }}>
                컨텐츠
              </Link>
            </div>
            <div className={cx("AllFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.ALLFEEDBACK}
                style={[2, 3].includes(props.id) ? { color: blue } : { color: grey }}
              >
                모든 피드백
              </Link>
            </div>
            <div className={cx("PosFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.POSFEEDBACK}
                style={props.id === 4 ? { color: blue } : { color: grey }}
              >
                긍정 피드백
              </Link>
            </div>
            <div className={cx("NegFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.NEGFEEDBACK}
                style={props.id === 5 ? { color: blue } : { color: grey }}
              >
                부정 피드백
              </Link>
            </div>
            <div className={cx("contentsFeedback")}>
              <Link
                className={cx("openFeedback")}
                onClick={setVideo}
                to={ROUTES.CONTENTSFEEDBACK}
                style={props.id === 8 ? { color: blue } : { color: grey }}
              >
                컨텐츠 요구 분석
              </Link>
            </div>
          </div>
          <div className={cx("openSetting")}>
            <Link to={ROUTES.SETTING} onClick={setVideo} style={props.id === 6 ? { color: blue } : { color: grey }}>
              환경설정
            </Link>
          </div>
          <div className={cx("openNotification")}>
            <Link to={ROUTES.NOTIFICATION} onClick={setVideo} style={props.id === 7 ? { color: blue } : { color: grey }}>
              알림
            </Link>
          </div>
        </div>
      </Fragment>
    );
  }
}

export default OpenSideBar;
