const metaData = [
  'title',
  'description',
  'link',
  'blog_title',
  'blog_link',
  'author',
  'publish_time'
];

export const formatDataSearch = (data) => {
  var array = [];
  var obj = {};
  for (var i = 0; i < data[0].length; i++) {
    for(var j = 0; j < metaData.length; j++) {
      obj[metaData[j]] = data[0][i][j+1];
    }
    array.push(Object.assign({}, obj));
    obj = {};
  }
  return array;
};

const includes = ['&nbsp;'];

export const formatString = (string) => {
  // Check string
  let check = string.includes(includes[0]);
  var count = (string.match(/&nbsp;/g) || []).length;
  if(check) {
    for (let i = 0; i<count; i++) {
      string = string.replace('&nbsp;',' ');
    }
    return string;
  }
  return string;
};