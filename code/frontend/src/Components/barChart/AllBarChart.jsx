import "./styles.css";
import React,{useEffect, useState} from "react";
import {
  BarChart,
  Bar,
  XAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import { useDispatch, useSelector } from "react-redux";
import { nowAnalysis } from 'store/modules/analysis';
import { actions } from "../../store/modules";

function AllBarChart() {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.user);
  
    const [analysisData, setAnalysisData] = useState([]);
    const isAnalysis = useSelector(nowAnalysis).analysisArray.clusters;

    const dataArray = []
    const object = {}
    function sortAnalysis() {
      console.log(isAnalysis)
      if (isAnalysis != undefined){
        dispatch(actions.setLoading(false))
      for (let i=10; i<isAnalysis.length; i++) {
        object[i] = {
          id: i-9,
          name: isAnalysis[i].top_comment.text_display,
          댓글수: isAnalysis[i].count,
          좋아요수: isAnalysis[i].like_count,
          box: 10,
          comment_id: isAnalysis[i].id,
          top_comment: isAnalysis[i].top_comment
        }
        dataArray.push(object[i])
      }
      setAnalysisData(dataArray)
      dispatch(actions.setAllTen(dataArray))
    } else {
      dispatch(actions.setLoading(true))
    }
    }

    useEffect(() => {
      sortAnalysis()
    },[isAnalysis])

    const CustomTooltip = ({ active, payload, label }) => {
      if (active && payload && payload.length) {
        return (
          <div
            className="custom-tooltip"
            style={{ width:"120%", lineHeight: "20px", border: "0.1px solid black", borderRadius: "20px" ,backgroundColor: "#fff", textAlign: "center" }}
          >
            <p className="label">{analysisData[Number(`${label}`)-1].name}</p>
            <p>
              {payload[1].name} {payload[1].value}
            </p>
            <p>
              {payload[3].name} {payload[3].value}
            </p>
          </div>
        );
      }
    
      return null;
    };

    return (
      <ResponsiveContainer width="90%" height="90%">
      <BarChart data={analysisData} margin={{ top: -40, right: 0, left: 0, bottom: 0 }} >
      <XAxis dataKey="id" interval={0} angle={0} dx={0} dy={10} />
        <Tooltip content={<CustomTooltip />} />
        <Bar
          dataKey="box"
          barSize={12}
          radius={[25, 25, 25, 25]}
          stackId="a"
          fill="#fff"
        />
        <Bar
          dataKey="댓글수"
          barSize={12}
          radius={[25, 25, 25, 25]}
          stackId="a"
          fill="#009C5B"
        />
        <Bar
          dataKey="box"
          barSize={12}
          radius={[25, 25, 25, 25]}
          stackId="a"
          fill="#fff"
        />
        <Bar
          dataKey="좋아요수"
          barSize={12}
          radius={[25, 25, 25, 25]}
          stackId="a"
          fill="#2DDA91"
        />
      </BarChart>
    </ResponsiveContainer>
    );
  }

  export default AllBarChart