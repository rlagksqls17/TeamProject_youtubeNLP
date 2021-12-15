import React from 'react';
import styles from './Notification.module.scss';
import classNames from 'classnames/bind';
import { Sidebar } from '../../../Components/common';

const cx = classNames.bind(styles);

function Notification() {
  const name = "이성효";
  return (
    <div className={cx('overviewContainer')}>
      <Sidebar id={7} />
      <div className={cx('sideLine')}></div>
      <div>
        <div className={cx('overViewTitle')}>반갑습니다 {name}님!</div>
        <div className={cx('overViewDescription')}>댓글들을 분석하고 사용자들의 피드백을 확인해보세요!</div>
        <div>NOTIFICATION</div>
      </div>
    </div>
  );
  }
  

export default Notification;
