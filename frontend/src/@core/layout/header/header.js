import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { list_navigation } from '@core/utils/db/links';
import './header.css';
import { Space140 } from '@core/components/atom/space/space';

function Navagation() {
  const listItems = list_navigation.map((item) => (
    <li key={item.name} className='item_nav'>
      <a className='link_nav' href={item.link}>
        {item.name}
      </a>
    </li>
  ));
  return <ul className='link__list-items-nav'>{listItems}</ul>;
}

export default function Header() {

  const [open, isOpen] = useState(false);
  const history = useHistory();
  useEffect(() => {
    window.onscroll = () => {
      scrollFunction();
    };
  }, []);

  const scrollFunction = () => {
    if (document.documentElement.scrollTop > 90) {
      document.getElementById('header_container').style.height = '70px';
    } else {
      document.getElementById('header_container').style.height = '90px';
    }
  };

  const isOpenNavigation = () => {
    document.getElementById('header-navigation').style.left = '0';
    isOpen(true);
  };

  const isCloseNavigation = () => {
    document.getElementById('header-navigation').style.left = '-100%';
    isOpen(false);
  };

  return (
    <div style={{position:'relative'}} className = {open? 'black' : ''}>
      <div className='header' id='header_container'>
        <div className='header__layout'>
          <div className='layout__logo' onClick={()=>history.push('/home')}>InfoCheck</div>
          <div className='layout__link'>{Navagation()}</div>
          <div className='layout__show-links'>
            <i className='bx bx-list-ul' onClick={() => {
              isOpenNavigation();
            }}></i>
          </div>
        </div>
      </div>
      <div
        className= {open? 'header__black' : ''}
        onClick={() => {isCloseNavigation();}}
      ></div>
      <div className='header__navigation' id='header-navigation'>
        <div className='navigation__list'>
          <div className='button__cancel'>
            <i className='bx bx-x' onClick={() => {isCloseNavigation();}}></i>
          </div>
          <ul className='list-links'>
            <li onClick={()=> history.push('/home')}><a href="#">Home</a></li>
            <li onClick={()=> history.push('/inference')}><a href="#">Inference</a></li>
            <li onClick={()=> history.push('/search')}><a href="#">Q and A</a></li>
          </ul>
        </div>
        <div className='navigation__cancel'></div>
      </div>
      <Space140></Space140>
    </div>
  );
}
