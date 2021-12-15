import React, { Fragment, useEffect, useState, useCallback } from "react";
import axios from "axios";
import classNames from "classnames/bind";
import styles from "./LoginPage.module.scss";
import { Navbar } from "Components/common";
import GoogleLogin from "react-google-login";
import loginPageImg from "img/loginPageImg.png";
import { UilEditAlt } from "@iconscout/react-unicons";
import { useHistory } from "react-router";
import ROUTES from "constants/routes";

import { useDispatch } from "react-redux";
import { actions } from "store/modules";

const cx = classNames.bind(styles);

function LoginPage() {
  const [clientId, setClientId] = useState(null);
  const [scope, setScope] = useState(null);
  const dispatch = useDispatch();
  const history = useHistory();
  const onLoginSuccess = (res: any) => {
    const code = res.code;
    requestSignin(code);
  };

  const logoutDispatch = useCallback(() => {
    dispatch(actions.resetAnalysisData());
    dispatch(actions.resetSelectedVideo());
    dispatch(actions.resetVideo());
    dispatch(actions.resetUserInfo());
  }, []);

  const requestSignin = (code: string) => {
    const signinForm = new FormData();
    signinForm.append("code", code);

    axios
      .post(process.env.REACT_APP_BACKEND_URL + "/api/auth/signin", signinForm)
      .then((response) => {
        // 로그인 성공 -> 홈으로
        const user_info = response.data;
        console.log(user_info);
        window.localStorage.setItem("token", user_info.access_token);
        dispatch(actions.loginSuccess({ success: Boolean(true) }));
        history.push(`${ROUTES.HOME}`);
      })
      .then(() => {
        axios
          .get(process.env.REACT_APP_BACKEND_URL + "/api/channels", {
            headers: {
              Authorization: `Bearer ${window.localStorage.getItem("token")}`,
            },
          })
          .then((response) => {
            const channelInfo = response.data.channel_items;

            if (channelInfo.length > 0) {
              console.log(channelInfo[0]);
              dispatch(
                actions.saveYoutubeInfo({
                  channelId: channelInfo[0].id,
                  channelUrl: channelInfo[0].channel_url,
                  channelTitle: channelInfo[0].title,
                  channelImgUrl: channelInfo[0].img_url,
                })
              );
            } else {
              alert("YouTube 채널이 존재하지 않습니다. 채널을 생성한 후에 다시 로그인 해주세요.");
              window.localStorage.removeItem("token");
              logoutDispatch();
            }
          })
          .catch((error) => {
            console.log(error);
          });
      })
      .catch((error) => {
        // 로그인 실패 -> 회원가입 페이지로
        const user_info = error.response.data;
        console.log(user_info);
        dispatch(actions.saveUser({ email: `${user_info.email}`, name: `${user_info.name}`, img_url: `${user_info.img_url}` }));
        history.push(`${ROUTES.SIGNUP}`);
        if (error.response.status === 403) {
          alert("토큰이 만료되었습니다! 다시 로그인 해주세요!");
          window.localStorage.removeItem("token");
          logoutDispatch();
        }
      });
  };

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_BACKEND_URL + "/api/oauth/clientinfo")
      .then((response) => {
        const scopeList = response.data.scopes;
        const scopeString = scopeList.join(" ");
        console.log(response.data);
        setClientId(response.data.client_id);
        setScope(scopeString);
      })
      .catch((error) => {
        if (error.response.status === 403) {
          alert("토큰이 만료되었습니다! 다시 로그인 해주세요!");
          window.localStorage.removeItem("token");
          logoutDispatch();
        }
      });
  }, []);

  return (
    <Fragment>
      <Navbar />
      <div className={cx("loginpagewrapper")}>
        <div className={cx("leftContainer")}>
          <img className={cx("leftImg")} src={loginPageImg} alt="" />
        </div>
        <div className={cx("rightContainer")}>
          <div className={cx("title")}>
            <div className={cx("pencilLogo")}>
              <UilEditAlt size="5vw" />
            </div>
            <div className={cx("titleText")}>EverReview</div>
          </div>
          <h1 className={cx("loginPageDoLogin")}>로그인하기</h1>
          <p className={cx("loginPageDescription")}>
            Google 계정으로 Evereview의 모든 서비스를 간편하게 이용하실 수 있습니다.
            <br />
            로그인하여 댓글 분석 서비스를 이용해보세요!
            <br />
            <br />
            댓글을 통해 시청자의 니즈를 파악하고,
            <br />
            피드백을 수용하여 더 좋은 컨텐츠를 만들어보세요.
          </p>
          {clientId && scope && (
            <div className={cx("loginBtn")}>
              <GoogleLogin
                clientId={clientId}
                buttonText="Sign In with Google"
                onSuccess={(result) => onLoginSuccess(result)}
                onFailure={(result) => console.log(result)}
                cookiePolicy={"single_host_origin"}
                responseType="code"
                accessType="offline"
                prompt="consent"
                scope={scope}
              />
            </div>
          )}
        </div>
      </div>
    </Fragment>
  );
}

export default LoginPage;
