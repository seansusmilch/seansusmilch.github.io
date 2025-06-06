import type { GiscusProps } from "@giscus/react";

export const SITE = {
  website: "https://seansusmilch.github.io", // replace this with your deployed domain
  author: "Sean",
  profile: "https://github.com/seansusmilch/",
  desc: "I mainly write about software development and homelab projects, but if a topic interests me enough, it might make it on here!",
  title: "Sean Susmilch",
  ogImage: undefined,
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: true,
  showBackButton: true,
  editPost: {
    enabled: false,
  },
};

export const GISCUS: GiscusProps = {
  repo: "seansusmilch/seansusmilch.github.io",
  repoId: "R_kgDOM6OIrA",
  category: "Post Comments",
  categoryId: "DIC_kwDOM6OIrM4ClqDn",
  mapping: "pathname",
  reactionsEnabled: "1",
  emitMetadata: "0",
  inputPosition: "bottom",
  lang: "en",
  loading: "lazy",
};

export const LOCALE = {
  lang: "en", // html lang code. Set this empty and default will be "en"
  timezone: "Asia/Bangkok", // Default global timezone (IANA format) https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
} as const;

export const LOGO_IMAGE = {
  enable: false,
  svg: false,
  width: 30,
  height: 30,
};
