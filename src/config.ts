export const SITE = {
  website: "https://seansusmilch.github.io", // replace this with your deployed domain
  author: "Sean",
  profile: "https://github.com/seansusmilch/",
  desc: "I mainly write about software development and homelab projects, but if a topic interests me enough, it might make it on here!",
  title: "Sean Susmilch",
  timezone: "America/Chicago",
  ogImage: undefined,
  dynamicOgImage: true,
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: true,
  showBackButton: true,
  editPost: {
    enabled: false,
    url: "",
    text: "",
  },
  lang: "en",
};

export const LOCALE = {
  lang: "en", // html lang code. Set this empty and default will be "en"
  timezone: "America/Chicago", // Default global timezone (IANA format) https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
} as const;

export const LOGO_IMAGE = {
  enable: false,
  svg: false,
  width: 30,
  height: 30,
};
