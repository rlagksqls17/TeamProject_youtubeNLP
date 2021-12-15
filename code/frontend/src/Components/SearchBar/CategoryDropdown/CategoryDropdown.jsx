import { useState } from 'react';
import classNames from 'classnames/bind';
import styles from './CategoryDropdown.module.scss';
import Select from 'react-select';
import { useDispatch, useSelector } from "react-redux";
import { nowCategory } from '../../../store/modules/category';
import { actions } from "../../../store/modules";

const cx = classNames.bind(styles);



function CategoryDropdown() {
  const [isClearable, setIsClearable] = useState(false)
  const [isDisabled, setIsDisabled] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isRtl, setIsRtl] = useState(true)
  const [isSearchable, setIsSearchable] = useState(false)

  const categoryOptions = [
    { value: '영상별 분석', label: '영상별 분석', rating: 'byVideo' },
    { value: '댓글 기간별 분석', label: '댓글 기간별 분석', rating: 'byComment' },
  ];

  const dispatch = useDispatch();
  const isCategorySelect = useSelector(nowCategory);

  const changeHandle = ( event ) => {
    const value = event.value
    console.log(value)
    if (value === '영상별 분석') {
      dispatch(actions.selectCategory('영상별 분석'))
    } else if (value === '댓글 기간별 분석'){
      dispatch(actions.selectCategory('댓글 기간별 분석'))
    }
    }
    

  return (
    <div className={cx("container")}>
      <div className={cx("menu-container")}>
      <Select
          className={cx("basic-single")}
          classNamePrefix="select"
          defaultValue={isCategorySelect === '영상별 분석' ? categoryOptions[1] : categoryOptions[0]}
          isDisabled={isDisabled}
          isLoading={isLoading}
          isClearable={isClearable}
          isRtl={isRtl}
          isSearchable={isSearchable}
          options={categoryOptions}
          onChange={changeHandle}
        />

        <div
          style={{
            color: 'hsl(0, 0%, 40%)',
            display: 'inline-block',
            fontSize: 12,
            fontStyle: 'italic',
            marginTop: '1em',
          }}
        >
        </div>
      </div>
    </div>
  );
}

export default CategoryDropdown;