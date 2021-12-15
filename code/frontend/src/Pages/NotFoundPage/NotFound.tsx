import React, { Fragment } from 'react';
import { Navbar } from '../../Components/common';
import styles from './NotFound.module.scss';
import classNames from 'classnames/bind';

const cx = classNames.bind(styles);

function NotFound() {
  return (
    <Fragment>
      <Navbar />
      <div className={cx('notfound')}>
        NotFound
      </div>
    </Fragment>
  );
}

export default NotFound;
