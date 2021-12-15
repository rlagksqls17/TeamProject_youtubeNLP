import "./styles.css";
import React from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer  
} from "recharts";

const data = [
  {
    id: 1,
    date: "11/23",
    name: "소리가 너무 커요",
    너무재밌어요: 251,
    화질구려요: 125,
    다음영상기대돼요: 62,
    box: 10
  },
  {
    id: 2,
    date: "11/24",
    name: "자막 틀렸어요",
    너무재밌어요: 512,
    화질구려요: 213,
    다음영상기대돼요: 632,
    box: 10
  },
  {
    id: 3,
    date: "11/25",
    name: "진짜 맛있어 보이네요",
    너무재밌어요: 123,
    화질구려요: 251,
    다음영상기대돼요: 245,
    box: 10
  },
  {
    id: 4,
    date: "11/26",
    name: "먹방 잘 찍으시네요",
    너무재밌어요: 349,
    화질구려요: 243,
    다음영상기대돼요: 243,
    box: 10
  },
  {
    id: 5,
    date: "11/27",
    name: "치킨먹어주세요",
    너무재밌어요: 52,
    화질구려요: 141,
    다음영상기대돼요: 632,
    box: 10
  },
  {
    id: 6,
    date: "11/28",
    name: "자세한 설명 굿",
    너무재밌어요: 241,
    화질구려요: 123,
    다음영상기대돼요: 252,
    box: 10
  },
  {
    id: 7,
    date: "11/29",
    name: "구독 누르고 갑니다",
    너무재밌어요: 251,
    화질구려요: 521,
    다음영상기대돼요: 222,
    box: 10
  },
  {
    id: 8,
    date: "11/30",
    name: "진짜 웃기다",
    너무재밌어요: 125,
    화질구려요: 11,
    다음영상기대돼요: 626,
    box: 10
  },
  {
    id: 9,
    date: "12/01",
    name: "화질 너무 구려요",
    너무재밌어요: 311,
    화질구려요: 6,
    다음영상기대돼요: 424,
    box: 10
  },
  {
    id: 10,
    date: "12/02",
    name: "음질이 너무 안좋아요",
    너무재밌어요: 422,
    화질구려요: 4,
    다음영상기대돼요: 571,
    box: 10
  }
];
const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div
          className="custom-tooltip"
          style={{ width:"120%", lineHeight: "10px", border: "0.1px solid black", borderRadius: "20px" ,backgroundColor: "#fff", textAlign: "center" }}
        >
          <p className="label">{label}</p>
          <p>
            {payload[0].name} {payload[0].value}
          </p>
          <p>
            {payload[1].name} {payload[1].value}
          </p>
          <p>
            {payload[2].name} {payload[2].value}
          </p>
        </div>
      );
    }
  
    return null;
  };
  
function AllLineChart() {
    return (
        <ResponsiveContainer width="90%" height="90%">
        <LineChart data={data} margin={{ top: 10, right: 20, left: 20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" interval={0} angle={0} dx={0} dy={10} />
          <Tooltip content={<CustomTooltip />} />
          <Line
            dataKey="너무재밌어요"
            type="monotone"
            fill="#009C5B"
          />
          <Line
            dataKey="화질구려요"
            type="monotone"
            fill="#4f4f4f"
          />
          <Line
            dataKey="다음영상기대돼요"
            type="monotone"
            fill="#2DDA91"
          />
        </LineChart>
      </ResponsiveContainer>
    );
  }

  export default AllLineChart