import React, { Fragment, useState } from "react";
import classNames from "classnames/bind";
import styles from "./SignUpPage.module.scss";
import { Navbar } from "Components/common";
import { SignUpStart, SignUpUserInfo, SignUpChannelInfo, SignUpFinish } from "../../Components/SignUp";

const cx = classNames.bind(styles);

function SignUpPage() {
  const [stepNum, setStepNum] = useState("1");
  const onSearchSubmit = (e: string) => {
    console.log(e);
    setStepNum(e);
  };
  return (
    <Fragment>
      <Navbar />
      {`${stepNum}` === "1" && <SignUpStart onSubmit={onSearchSubmit} />}
      {`${stepNum}` === "2" && <SignUpUserInfo onSubmit={onSearchSubmit} />}
      {`${stepNum}` === "3" && <SignUpChannelInfo onSubmit={onSearchSubmit} />}
      {`${stepNum}` === "4" && <SignUpFinish onSubmit={onSearchSubmit} />}
    </Fragment>
  );
}

export default SignUpPage;
