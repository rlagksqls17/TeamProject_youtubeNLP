import { useEffect,useState, forwardRef } from 'react';
import classNames from 'classnames/bind';
import styles from './CommentDropdown.module.scss';
import DatePicker from "react-datepicker";
import { useSelector, useDispatch } from 'react-redux';
import { nowDate } from '../../../store/modules/date';
import { actions } from "../../../store/modules";


const cx = classNames.bind(styles);


function CommentDropdown() {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const dispatch = useDispatch();
  const isDate = useSelector(nowDate);
  useEffect(() => {
    dispatch(actions.saveDate({ startDate: startDate, endDate: endDate}));
    return () => {
      const dateYear = startDate.getFullYear()
      const dateMonth = startDate.getMonth()+1
      const dateDate = startDate.getDate()
    };
  }, [startDate, endDate, dispatch, isDate]);

  const CustomInput = forwardRef(({ value, onClick }, ref) => (
    <button className={cx("datePick1")} onClick={onClick} ref={ref}>
      {value}
    </button>
  ));
  const handleClickStart = (e) => {
    e.preventDefault();
  };
  const handleClickEnd = (e) => {
    e.preventDefault();
  };

  const CustomInput2 = forwardRef(({ value, onClick }, ref) => (
    <button className={cx("datePick2")} onClick={onClick} ref={ref}>
      {value}
    </button>
  ));



    return (
      <div className={cx("searchContainer")}>
        <div className={cx("menu-container")}>
          <div className={cx("commentSearchWrap")}>
            <div className={cx("commentSearchBar")} onClick={handleClickStart}>
              
              <DatePicker
                selected={startDate}
                onChange={(date) => setStartDate(date)}
                customInput={<CustomInput />}
                maxDate = {endDate}
              />
            </div>
            <div className={cx("commentSearchBar")} onClick={handleClickEnd}>
            
            <DatePicker
              selected={endDate}
              onChange={(date) => setEndDate(date)}
              customInput={<CustomInput2 />}
              minDate = {startDate}
            />
            </div>
          </div>
        </div>
      </div>
    );
}

export default CommentDropdown;