import React, { Reducer, useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import ROUTES from "constants/routes";
import styles from "./Navbar.module.scss";
import classNames from "classnames/bind";
import logo from "img/logo_transparent.png";
import { actions } from "store/modules";
import { useDispatch, useSelector } from "react-redux";
import { ReducerType } from "store/modules";
import { NavBarProfile } from "./NavBarProfile";
import axios from "axios";
const cx = classNames.bind(styles);

function Navbar() {
  const dispatch = useDispatch();
  const isLogin = useSelector<ReducerType>((state) => state.user.success);
  const [imgUrl, setImgUrl] = useState("" as string);
  const [nickName, setNickName] = useState("" as string);

  const logoutDispatch = useCallback(() => {
    dispatch(actions.resetAnalysisData());
    dispatch(actions.resetSelectedVideo());
    dispatch(actions.resetVideo());
    dispatch(actions.resetUserInfo());
  }, []);
  const category: string[] = ["먹방", "일상", "리뷰", "게임", "피트니스", "ASMR", "주식", "부동산", "이슈", "교육", "기타"];
  var categoryNumList: number[] = [];
  const loginDispatch = useCallback((userInfo) => {
    categoryNumList = userInfo.contents_category.map((element: string) => {
      return category.indexOf(element);
    });
    dispatch(
      actions.saveAllUserInfo({
        email: userInfo.email,
        name: userInfo.name,
        img_url: userInfo.img_url,
        nickName: userInfo.nickname,
        category: userInfo.contents_category,
        categoryNumList: categoryNumList,
        upload_term: userInfo.upload_term,
        inputName: "",
      })
    );
    console.log(userInfo.contents_category);
  }, []);

  const getUserInfo = () => {
    axios
      .get(process.env.REACT_APP_BACKEND_URL + "/api/user", {
        headers: {
          Authorization: `Bearer ${window.localStorage.getItem("token")}`,
        },
      })
      .then((response) => {
        console.log(response.data);
        const userInfo = response.data;
        loginDispatch(userInfo);
        setImgUrl(userInfo.img_url);
        setNickName(userInfo.nickname);
      })
      .catch((error) => {
        alert("토큰이 만료되었습니다! 다시 로그인 해주세요!");
        window.localStorage.removeItem("token");
        logoutDispatch();
      });
  };

  useEffect(() => {
    if (isLogin) {
      getUserInfo();
    }
  }, [isLogin]);

  return (
    <div className={cx("header")}>
      <Link className={cx("logo")} to={ROUTES.HOME}>
        <img style={{ width: "auto", height: "55px" }} src={logo} alt="logo" />
      </Link>
      <div className={cx("linkWrapper")}>
        <Link className={cx("link")} to={ROUTES.HOME}>
          Home
        </Link>
        <Link className={cx("link")} to={ROUTES.ABOUT}>
          About
        </Link>

        {!isLogin && (
          <Link className={cx("link")} to={ROUTES.LOGIN}>
            Login
          </Link>
        )}

        {isLogin && (
          <Link className={cx("link")} to={ROUTES.DASHBOARD}>
            DashBoard
          </Link>
        )}
      </div>
      {isLogin && (
        <div className={cx("navBarProfile")}>
          <NavBarProfile img_url={imgUrl} nickname={nickName} />
        </div>
      )}
    </div>
  );
}

export default Navbar;
