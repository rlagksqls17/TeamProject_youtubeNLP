import React, { useState, useCallback } from "react";
import { Link } from "react-router-dom";
import ROUTES from "../../../constants/routes";
import styles from "./Sidebar.module.scss";
import classNames from "classnames/bind";
import OpenSideBar from "./OpenSidebar";
import {
  UilDashboard,
  UilChart,
  UilUserCircle,
  UilSetting,
  UilBell,
  UilReact,
  UilSignOutAlt,
  UilUserSquare,
  UilAngleDoubleRight,
  UilAngleDoubleLeft,
} from "@iconscout/react-unicons";
import { useDispatch, useSelector } from "react-redux";
import { actions } from "../../../store/modules";

const cx = classNames.bind(styles);

function Sidebar(props) {
  const dispatch = useDispatch();
  const img_url = useSelector((state) => state.user.img_url);
  const grey = "#2f2f2f50";
  const blue = "#6563FF";
  const [isActive, setActive] = useState(false);
  const logOut = useCallback(() => {
    dispatch(actions.resetAnalysisData());
    dispatch(actions.resetSelectedVideo());
    dispatch(actions.resetVideo());
    dispatch(actions.resetUserInfo());
  }, []);
  const handleToggle = () => {
    setActive(!isActive);
  };
  const setVideo = () => {
    dispatch(actions.selectCategory("영상별 분석"));
  };
  const propsArray = [2, 3, 4, 5, 8];
  return (
    <>
      <div className={cx("sideBarContainer")}>
        <div className={cx("sideLogo")}>
          <Link className={cx("logo")} to={ROUTES.HOME} onClick={setVideo}>
            <UilReact className={cx("sideLogoImage")} />
          </Link>
          <div className={cx("openButton")}>
            {isActive ? <UilAngleDoubleLeft onClick={handleToggle} /> : <UilAngleDoubleRight onClick={handleToggle} />}
          </div>
        </div>
        <div className={cx("sideIcon")}>
          <Link className={cx("logo")} to={ROUTES.DASHBOARD} onClick={setVideo}>
            <UilDashboard className={cx("sideDashBoard")} style={props.id === 1 ? { color: blue } : { color: grey }} />
          </Link>
          <Link className={cx("logo")} to={ROUTES.ALLFEEDBACK} onClick={setVideo}>
            <UilChart className={cx("sideContents")} style={propsArray.includes(props.id) ? { color: blue } : { color: grey }} />
          </Link>
          <Link className={cx("logo")} to={ROUTES.SETTING} onClick={setVideo}>
            <UilSetting className={cx("sideSetting")} style={props.id === 6 ? { color: blue } : { color: grey }} />
          </Link>
          <Link className={cx("logo")} to={ROUTES.NOTIFICATION} onClick={setVideo}>
            <UilBell className={cx("sideNotification")} style={props.id === 7 ? { color: blue } : { color: grey }} />
          </Link>
        </div>
        <div className={cx("sideProfile")}>
          <Link className={cx("logo")} to={ROUTES.PROFILE} onClick={setVideo}>
            <img className={cx("sideUser")} src={img_url} alt="user_profile_img" />
          </Link>

          <Link className={cx("logo")} to={ROUTES.HOME} onClick={logOut}>
            <UilSignOutAlt className={cx("sideLogout")} />
          </Link>
        </div>
      </div>
      <OpenSideBar isActive={isActive} id={props.id} />
    </>
  );
}

export default Sidebar;
