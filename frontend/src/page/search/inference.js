import React from 'react';
import './search.css';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { searchInference } from '@core/utils/api/api';
import { Space40, Space60, Space120 } from '@core/components/atom/space/space';
import { Spinner } from 'react-bootstrap';

const labelReplaction= {
  "refute":"Bác bỏ",
  "support":"Ủng hộ",
  "neutral":"Trung lập"
}
export default class Inference extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      number: 4,
      data: [],
      percent: 0,
      tracking: false,
      isSearch: false,
      disable: true,
      error: false,
    };
  }

  componentDidMount() {
    AOS.init({
      once: true
    });
    document.title = 'InfoCheck | Inference';
  }

  render() {
    const { text, data, isSearch, error } = this.state;
    return (
      <div>
        <div
          data-aos='fade-up'
          data-aos-easing='ease-in-sine'
          data-aos-duration='600'
          className='search__title'>
          <div className='title__layout'>
            <h1 className='highlight-color'>Inference</h1>
          </div>
        </div>
        <div
          data-aos='fade-up'
          data-aos-easing='ease-in-sine'
          data-aos-duration='600'
          className='search__description'>
        </div>
        <Space40></Space40>
        <div
          data-aos='fade-right'
          data-aos-easing='ease-in-sine'
          data-aos-duration='600'
          data-aos-delay='600'
          className='search'>
          <div className='search__layout'>
            <input
              className='input-search'
              id='input-search'
              placeholder='Nhập thông tin cần chứng thực ở đây'
              onChange={async (event) => {
                await this.setState({ text: event.target.value });
                if (text.length > 0) {
                  await this.setState({ disable: false });
                } else {
                  this.setState({ disable: true });
                }
              }}
            />
            <button
              className='btn-search'
              // disabled={disable}
              onClick={async () => {

                if (text.length === 0) {
                  this.setState({ error: true });
                  return;
                }
                this.setState({ isSearch: true });
                let bodyFormData = new FormData();
                bodyFormData.append('data', text);
                const res = await searchInference(bodyFormData);
                console.log(res);
                if (!res.data.data.length) {
                  this.setState({ error: true });
                  this.setState({ isSearch: false });
                  return;
                }
                await this.setState({ data: res.data.data });
                await this.setState({ isSearch: false });
                await this.setState({ disable: true });
                document.getElementById('input-search').value = '';
              }}
            >
              <div className='btn-search__layout'>
                <div className='txt-search'>Kiểm tra</div>
                {isSearch ?
                  <Spinner animation='border' role='status' size='sm' variant='light' className='spinner-custom'>
                    <span className='visually-hidden'>Loading...</span>
                  </Spinner>
                  :
                  <div></div>
                }
              </div>
            </button>
          </div>
          {text && <><b>Thông tin cần kiểm tra : </b><div style={{width:"53%",display:"flex",flexDirection:"row",justifyContent:"center", fontSize: "18px"}}> {text}</div> <div style={{ marginTop: '16px' }}></div></>}
          {error ? <div className='search__error'><i className='bx bx-error'></i> Request server error. Please try again!</div> : <div style={{ marginTop: '16px' }}></div>}
          {data.length > 0 && <><div><b>Số lượng đánh giá: {data.length}</b></div>
            <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between", width: "30%", fontWeight: "bold" }}><div style={{color: 'rgb(44, 151, 12)', fontSize: "18px"}}>Ủng hộ : {data.filter(item => item.label == 'support').length}</div><div style={{color:'rgb(255, 2, 2)', fontSize: "18px"}}>Bác bỏ: {data.filter(item => item.label == 'refute').length}</div><div style={{color:'rgb(194, 194, 23)', fontSize: "18px"}}>Trung lập: {data.filter(item => item.label == 'neutral').length}</div></div></>}
        </div>
        {data.length > 0 && data.sort((a,b)=>{
         if(a.label[0]>b.label[0]){
          return -1;
         }else if(a.label[0]<b.label[0]){
          return 1;
         }
          return 0;
        }).map(item => (<div className='search__result' key={item.sent_id}>

          <div className='result'>
            <h5><span style={{ fontWeight: "bold" }}>Kết quả đánh giá:</span> <span className={item.label} style={{ fontWeight: "bold" }}>{labelReplaction[item.label]}</span></h5>
            <div>
              <span style={{ fontWeight: "bold" }}>Mức độ tin cậy của đánh giá:</span> {(item.inference_score*100).toFixed(3)}%
            </div>
            <div>
              <span style={{ fontWeight: "bold" }}>Minh chứng:</span> {item.evidence}
            </div>
            <div> <span style={{ fontWeight: "bold" }}>Tài liệu dựa vào : </span> <span dangerouslySetInnerHTML={{ __html: item.context.content.replace(item.evidence, `<b>${item.evidence}</b>`) }}>
            </span></div>
          </div>
        </div>))}
        <Space60></Space60>
        <div
          data-aos='fade-up'
          data-aos-easing='ease-in-sine'
          data-aos-duration='600'
          data-aos-delay='1200'
          className='title-result'>
          <h5 className='txt-result'>
            Hãy bắt đầu kiểm tra chứng thực thông tin của bạn
          </h5>
          <Space40></Space40>
        </div>
        <Space120></Space120>
      </div>
    );
  }
}
