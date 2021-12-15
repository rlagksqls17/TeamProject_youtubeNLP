import React, { useState } from "react";
import styles from "./SignUpUserInfo.module.scss";
import classNames from "classnames/bind";
import { UilEditAlt } from "@iconscout/react-unicons";
import { useDispatch } from "react-redux";
import { actions } from "store/modules";

const cx = classNames.bind(styles);

type InputValue = string | number | ReadonlyArray<string>;

function SignUpUserInfo(props: any) {
  const dispatch = useDispatch();

  const [inputName, setInputName] = useState<InputValue>("");
  const [nickName, setNickName] = useState<InputValue>("");

  const clickEventHandler = (e: any) => {
    e.preventDefault();
    console.log(inputName, nickName);
    dispatch(actions.saveName({ inputName: `${inputName}`, nickName: `${nickName}` }));
    props.onSubmit("3");
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
            <div className={cx("nowStepBox")}>2</div>
            <div className={cx("link")}></div>
            <div className={cx("stepBox")}>3</div>
            <div className={cx("link")}></div>
            <div className={cx("stepBox")}>4</div>
          </div>
          <p className={cx("infoTitle")}>회원 정보 입력</p>

          <div className={cx("inputContainer")}>
            <label id="name" htmlFor="name">
              성명
            </label>
            <input id="name" type="text" value={inputName} onChange={(e) => setInputName(e.target.value)} />
          </div>

          <div className={cx("inputContainer")}>
            <label id="nickName" htmlFor="nickName">
              별명
            </label>
            <input id="nickName" type="text" value={nickName} onChange={(e) => setNickName(e.target.value)} />
          </div>

          <button disabled={!(inputName && nickName)} className={cx("btn")} onClick={clickEventHandler}>
            다음 단계
          </button>
        </div>
      </div>
    </>
  );
}

export default SignUpUserInfo;
