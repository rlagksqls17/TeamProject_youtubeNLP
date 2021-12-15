import styles from "./NavBarProfile.module.scss";
import classNames from "classnames/bind";
import ROUTES from "constants/routes";
import axios from "axios";
import { useEffect, useState, useRef, useCallback } from "react";
import { actions } from "store/modules";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router";

const cx = classNames.bind(styles);

type NavBarProfileProps = {
  img_url: string;
  nickname: string;
};

type refType = HTMLDivElement | null | any;

const NavBarProfile: React.FC<NavBarProfileProps> = ({ img_url, nickname }) => {
  const dispatch = useDispatch();
  const history = useHistory();
  const modalEl = useRef<refType>(null);
  const [active, setActive] = useState(Boolean(false));
  const [isOpen, setIsOpen] = useState(Boolean(true));

  const clickHandler = () => {
    if (active) {
      setActive(Boolean(false));
      setIsOpen(Boolean(false));
    } else {
      setActive(Boolean(true));
      setIsOpen(Boolean(true));
    }
  };

  const goProfile = () => {
    history.push(ROUTES.PROFILE);
  };

  const logoutDispatch = useCallback(() => {
    dispatch(actions.resetAnalysisData());
    dispatch(actions.resetSelectedVideo());
    dispatch(actions.resetVideo());
    dispatch(actions.resetUserInfo());
  }, []);

  const logoutHandler = () => {
    axios
      .get(process.env.REACT_APP_BACKEND_URL + "/api/auth/signout", {
        headers: {
          Authorization: `Bearer ${window.localStorage.getItem("token")}`,
        },
      })
      .then((response) => {
        console.log(response.data);
        window.localStorage.removeItem("token");
        logoutDispatch();
      })
      .catch((error) => {
        if (error.response.status === 403) {
          alert("토큰이 만료되었습니다! 다시 로그인 해주세요!");
          logoutDispatch();
        }
      });
  };

  const handleCloseModal = (e: any) => {
    if (isOpen && modalEl?.current && !modalEl?.current?.contains(e.target as Node)) {
      setActive(Boolean(false));
    }
  };

  const handleCloseModalUp = (e: any) => {
    if (!isOpen && modalEl?.current && modalEl?.current?.contains(e.target as Node)) {
      setIsOpen(Boolean(true));
    }
  };

  useEffect(() => {
    window.addEventListener("click", handleCloseModal);
    window.addEventListener("mousedown", handleCloseModalUp);
    return () => {
      window.removeEventListener("click", handleCloseModal);
      window.removeEventListener("mousedown", handleCloseModalUp);
    };
  }, []);

  return (
    <>
      <div className={cx("navBarProfileTop")} ref={modalEl} onClick={clickHandler}>
        <div className={cx("profileImg")}>
          <img src={img_url} alt="profile_img" />
        </div>
        <div className={cx("profileName")}>{nickname}</div>
      </div>
      {active && (
        <div className={cx("navBarProfileDropdown")}>
          <div className={cx("navBarProfileDropdownMenu")} onClick={goProfile}>
            사용자 정보
          </div>
          <div className={cx("navBarProfileDropdownMenu")} onClick={logoutHandler}>
            로그아웃
          </div>
        </div>
      )}
    </>
  );
};
export default NavBarProfile;
