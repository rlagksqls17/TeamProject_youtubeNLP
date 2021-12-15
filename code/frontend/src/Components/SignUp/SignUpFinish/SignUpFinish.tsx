import React from "react";
import ROUTES from "constants/routes";
import styles from "./SignUpFinish.module.scss";
import classNames from "classnames/bind";
import { UilEditAlt } from "@iconscout/react-unicons";
import { useHistory } from "react-router";
import { useSelector } from "react-redux";
import { ReducerType } from "store/modules";
import axios from "axios";

const cx = classNames.bind(styles);

function SignUpFinish(props: any) {
  const history = useHistory();
  const email: any = useSelector<ReducerType>((state) => state.user.email);
  const img_url: any = useSelector<ReducerType>((state) => state.user.img_url);
  const inputName: any = useSelector<ReducerType>((state) => state.user.inputName);
  const nickName: any = useSelector<ReducerType>((state) => state.user.nickName);
  const category: any = useSelector<ReducerType>((state) => state.user.category);
  const upload_term: any = useSelector<ReducerType>((state) => state.user.upload_term);

  const submitUserInfo = () => {
    const userInfoForm = new FormData();
    userInfoForm.append("email", email);
    userInfoForm.append("name", inputName);
    userInfoForm.append("nickname", nickName);
    userInfoForm.append("img_url", img_url);
    userInfoForm.append("upload_term", upload_term);
    userInfoForm.append("contents_category", category);

    axios
      .post(process.env.REACT_APP_BACKEND_URL + "/api/auth/signup", userInfoForm)
      .then((response) => {
        //로그인 성공
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const clickEventHandler = (e: any) => {
    e.preventDefault();
    props.onSubmit("");
    submitUserInfo();
    history.push(ROUTES.LOGIN);
  };

  return (
    <>
      <div className={cx("wrapper")}>
        <div className={cx("container")}>
          <div className={cx("title")}>
            <div className={cx("pencilLogo")}>
              <UilEditAlt size="80" />
            </div>
            <div className={cx("titleText")}>EverReview</div>
          </div>

          <div className={cx("stepContainer")}>
            <div className={cx("stepBox")}>1</div>
            <div className={cx("link")}></div>
            <div className={cx("stepBox")}>2</div>
            <div className={cx("link")}></div>
            <div className={cx("stepBox")}>3</div>
            <div className={cx("link")}></div>
            <div className={cx("nowStepBox")}>4</div>
          </div>

          <div className={cx("completeCheck")}>✔</div>

          <p className={cx("welcomeText")}>{inputName} 님, 환영합니다!</p>
          <p>EVEREVIEW의 수 많은 서비스를 이용해보세요!</p>
          <button className={cx("finish_btn")} onClick={clickEventHandler}>
            로그인하러 가기
          </button>
        </div>
      </div>
    </>
  );
}

export default SignUpFinish;
