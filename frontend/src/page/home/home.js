import React from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import './home.css';
import LKH from '@core/assets/images/lkh.png';
import LTQT from '@core/assets/images/tree.jpg';
import THT from '@core/assets/images/tree.jpg';
import { Space120 } from '@core/components/atom/space/space';
export default class Home extends React.Component {
  componentDidMount() {
    AOS.init();
    document.title = 'InfoCheck | Home';
  }

  render() {
    return (
      <div className='home'>
        <div className='home__header-content'>
          <div className='header-content'>
            <div className='header-content__box-title'>
              <div
                data-aos='fade-right'
                data-aos-easing='ease-in-sine'
                data-aos-duration='1000'
                className='box-title__title'>
                <h1>
                  <br/>
                  Do you need to
                  <span className='title--modifile'> Check your infomation </span>
                  or
                  <span className='title--modifile'> Q&A </span></h1>
              </div>
              <div
                data-aos='fade-up'
                data-aos-easing='ease-in-sine'
                data-aos-delay='1000'
                data-aos-duration='700'
                className='box-title__group-button'>
                <div className='btn btn-documents' onClick={()=> this.props.history.push('/inference')}>
                  <span>Inference</span> <span className='icon_arrow'><i className='bx bx-right-arrow-alt'></i></span>
                </div>
                <div className='btn btn-tracking' onClick={()=> this.props.history.push('/search')}>
                  <span>Q&A</span>
                  <span className='icon_arrow'>
                    <i className='bx bx-right-arrow-alt'></i>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Space120></Space120>
        <div
          data-aos='fade-up'
          data-aos-easing='ease-in-sine'
          data-aos-duration='800'
          data-aos-offset='180'
          className='home__thanks'>
          <h1 className='thanks__title title'>
            Thank You, <span className='title--modifile'>Mentor!</span>
          </h1>
          <div className='thanks__description'>
            <p className='description'>Thanks for being a good mentor and for guiding me on the right path. I will always be thankful to you.</p>
          </div>
          <div className='thanks__card'>
            <div
              className='card__image'>
              <img src={LKH} alt='le kim hung'/>
            </div>
            <p className='card__title-name'><span className='title--modifile'>PhD.</span> Lê Kim Hùng</p>
            <div
              data-aos='fade-up'
              data-aos-easing='ease-in-sine'
              data-aos-offset='180'
              data-aos-duration='800'
              className='card__description'>
              <p className='description'>
                <span className='description__1'>Besides teaching, Mr. Hung actively promotes the scientific research movement among students by organizing a research group named IEC (Intelligent Edge Computing). The group focuses on research and development on artificial intelligence (AI) applications in IoT and Edge Computing models.</span>
              With him, promoting the scientific research movement among students is extremely important, helping students to develop both in terms of research mindset and creativity. very helpful in your development path in the future.
              </p>
            </div>
          </div>
        </div>
        <Space120></Space120>
        <div
          data-aos='fade-up'
          data-aos-easing='ease-in-sine'
          data-aos-offset='240'
          data-aos-duration='800'
          className='home__project'>
          <h1 className='project__title title'>Project <span className='title--modifile'>Team</span></h1>
          <div className='project__layout-members'>
            <div className='members'>
              <div className='members__member'>
                <div className='member__card'>
                  <div
                    className='card__image-student'>
                    <img src={LTQT} alt='Le Trinh Quang Trieu'/>
                  </div>
                  <p className='card__title-name'><span className='title--modifile'>Student.</span> Nguyễn Hoàng Long</p>
                </div>
              </div>
              <div className='members__member'>
                <div className='member__card'>
                  <div
                    className='card__image-student'>
                    <img src={THT} alt='Le Trinh Quang Trieu'/>
                  </div>
                  <p className='card__title-name'><span className='title--modifile'>Student.</span> Trịnh Huỳnh Trọng Nhân</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Space120></Space120>
      </div>
    );
  }
}
