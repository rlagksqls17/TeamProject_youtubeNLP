import React from 'react';
import NLayer1 from '../../img/animationImg/Layer1.png';
import NLayer2 from '../../img/animationImg/Layer2.png';
import NLayer3 from '../../img/animationImg/Layer3.png';
import NLayer4 from '../../img/animationImg/Layer4.png';
import NLayer5 from '../../img/animationImg/Layer5.png';
import NLayer6 from '../../img/animationImg/Layer6.png';
import NLayer7 from '../../img/animationImg/Layer7.png';
import NLayer8 from '../../img/animationImg/Layer8.png';
import NLayer9 from '../../img/animationImg/Layer9.png';
import NLayer10 from '../../img/animationImg/Layer10.png';
import NLayer11 from '../../img/animationImg/Layer11.png';
import NLayer12 from '../../img/animationImg/Layer12.png';
import NLayer13 from '../../img/animationImg/Layer13.png';
import NLayer14 from '../../img/animationImg/Layer14.png';
import NLayer15 from '../../img/animationImg/Layer15.png';
import styles from './Animation.module.scss';
import classNames from 'classnames/bind';
const cx = classNames.bind(styles);

function AnimationPage(): JSX.Element {
    return (
          <div className={cx('imgWrap')}>
            <img className={cx('NLayer1')} src={NLayer1} alt='' />
            <img className={cx('NLayer14')} src={NLayer14} alt='' />
            <img className={cx('NLayer13')} src={NLayer13} alt='' />
            <img className={cx('NLayer12')} src={NLayer12} alt='' />
            <img className={cx('NLayer11')} src={NLayer11} alt='' />
            <img className={cx('NLayer2')} src={NLayer2} alt='' />
            <img className={cx('NLayer4')} src={NLayer7} alt='' />
            <img className={cx('NLayer5')} src={NLayer6} alt='' />
            <img className={cx('NLayer6')} src={NLayer5} alt='' />
            <img className={cx('NLayer7')} src={NLayer4} alt='' />
            <img className={cx('NLayer3')} src={NLayer3} alt='' />
            <img className={cx('NLayer9')} src={NLayer9} alt='' />
            <img className={cx('NLayer10')} src={NLayer10} alt='' />
            <img className={cx('NLayer8')} src={NLayer8} alt='' />
            <img className={cx('NLayer15')} src={NLayer15} alt='' />
          </div>
    );
  }
  
  export default AnimationPage;
  