import { useEffect, useState } from "react";
import classNames from "classnames/bind";
import styles from "./SearchDropdown.module.scss";
import { useSelector, useDispatch } from "react-redux";
import { actions } from "../../../store/modules";
import { nowSelectedVideoList } from "../../../store/modules/selectedVideo";
import { nowVideoList, nowNextVideoPage, nowPrevVideoPage } from "../../../store/modules/video";
import * as Hangul from "hangul-js";
import { useRef } from "react";
import _, { debounce } from "lodash";
import axios from "axios";

const cx = classNames.bind(styles);

function VideoDropdown(props) {
  const dispatch = useDispatch();
  const modalRef = useRef();
  const isSelectedVideoList = useSelector(nowSelectedVideoList);
  const isVideoList = useSelector(nowVideoList);

  const user = useSelector((state) => state.user);
  const channel_id = user.channelUrl.substring(32);
  const handleBtn = (btnId) => (e) => {
    e.preventDefault();
    dispatch(actions.selectSelectedVideo(btnId));
  };

  const handleClickClose = (btnId) => (e) => {
    e.preventDefault();
    dispatch(actions.closeSelectedVideo(btnId));
  };

  const handleClickCloseAll = () => {
    Object.keys(isSelectedVideoList.selectedVideoList).map((keyName, i) => dispatch(actions.closeSelectedVideo(keyName)));
    props.setSearchWord("");
  };

  const handleClickSelectAll = () => {
    Object.keys(isSelectedVideoList.selectedVideoList).map((keyName, i) => dispatch(actions.selectAllSelectedVideo(keyName)));
  };

  function compareWord(origin) {
    let compareTitle = origin;
    let filteredTitle = Hangul.disassemble(compareTitle, true);
    console.log(props.searchWord);
    let chosung = "";
    for (var i = 0, l = filteredTitle.length; i < l; i++) {
      chosung += filteredTitle[i][0];
    }
    return chosung;
  }

  const isNextVideoPage = useSelector(nowNextVideoPage);
  const isPrevVideoPage = useSelector(nowPrevVideoPage);

  // async function getVideos() {
  //   const response = await axios.get(process.env.REACT_APP_BACKEND_URL + `/api/videos/?channel_id=${channel_id}&page_token=${isNextVideoPage}`, {
  //     headers: {
  //       'Authorization': `Bearer ${window.localStorage.getItem("token")}`,
  //     },
  //   })
  //   .then(response => {
  //     if (response.data.prev_page_token == null){
  //       dispatch((actions.updateSelectedVideoList({selectedVideoList:Array(response.data.page_info.totalResults).fill(false)})));
  //       dispatch((actions.updateVideoList(response.data.video_items)))
  //       dispatch((actions.setNextVideoPage(response.data.next_page_token)))
  //     } else if (response.data.prev_page_token != null ){
  //       let testArr = [...isVideoList];
  //       dispatch((actions.updateVideoList(testArr.concat(response.data.video_items))))
  //       dispatch((actions.setNextVideoPage(response.data.next_page_token)))
  //     } else if (isPrevVideoPage == null && isNextVideoPage == null ) {
  //       console.log("Done!")
  //     }
  //   })
  //   .catch(error => {
  //     console.log(error)
  //   });
  //   console.log(response)
  // }

  const modalScroll = _.debounce(() => {
    const { scrollHeight, scrollTop, clientHeight } = modalRef.current;
    if (scrollHeight && scrollTop && clientHeight && scrollHeight - 10 < scrollTop + clientHeight) props.func();
  }, 100);

  return (
    <>
      <div className={cx("videoContainer")}>
        {/* <div className={cx("selectAll")} onClick={handleClickSelectAll}>/</div> ​*/}

        <div className={cx("deleteAll")} onClick={handleClickCloseAll}>
          X
        </div>
        <div className={cx("videoHeader")}>
          {isSelectedVideoList.selectedVideoList &&
            Object.keys(isSelectedVideoList.selectedVideoList).map((keyName, i) =>
              isSelectedVideoList.selectedVideoList[keyName] ? (
                <div className={cx("videoHeaderBox")} onClick={!undefined && handleClickClose(i)} key={i}>
                  {!undefined && isVideoList[i]["title"].substr(0, 10)}
                  <span>x</span>{" "}
                </div>
              ) : null
            )}
        </div>
        <div className={cx("videoItems")} ref={modalRef} onScroll={modalScroll}>
          {isVideoList &&
            isVideoList
              .filter((val) => {
                if (props.searchWord && props.searchWord == "") {
                  return val;
                } else if (
                  val.title.toLowerCase().includes(props.searchWord.toLowerCase()) ||
                  Hangul.search(val.title.toLowerCase(), props.searchWord.toLowerCase()) > -1 ||
                  compareWord(val.title.toLowerCase()).includes(props.searchWord.toLowerCase())
                ) {
                  return val;
                }
                return false;
              })
              .map((videoInfo, i) => {
                return (
                  <div
                    className={cx(`videoItem_${isSelectedVideoList.selectedVideoList[videoInfo.id - 1]}`)}
                    id="videoItem"
                    onClick={!undefined && handleBtn(i)}
                    style={{ backgroundColor: isSelectedVideoList.selectedVideoList[i] ? "#D0E9FF" : "#ffffff" }}
                    key={i}
                  >
                    <div className={cx("videoImageWrap")}>
                      <img className={cx("videoImage")} src={videoInfo.thumbnail_url} alt="imgUrl" />
                    </div>
                    <div className={cx("videoImageText")}>
                      제목 : {!undefined && videoInfo.title} <br />
                      상세 내용 : 상세 내용 <br />
                      조회 수 : {!undefined && videoInfo.view_count} 회 <br />
                      댓글 수 : {!undefined && videoInfo.comment_count} 개 <br />
                      좋아요 수 : {!undefined && videoInfo.like_count} 개 <br />
                      업로드 시간 : {!undefined && new Date(videoInfo.published_at).toLocaleString()} <br />
                    </div>
                  </div>
                );
              })}
        </div>
      </div>
    </>
  );
}

export default VideoDropdown;
